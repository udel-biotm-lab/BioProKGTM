# -*- coding: utf-8 -*-
from __future__ import unicode_literals, print_function
#from importlib import reload
import os
import sys
reload(sys);
import pandas as pd
sys.setdefaultencoding("utf8")
import json
import itertools

# nlputis codes.
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from protolib.python import document_pb2, rpc_pb2, edgRules_pb2
from utils.rpc.iterator import request_iter_docs, edg_request_iter_docs
from utils.rpc import grpcapi
from utils.helper import DocHelper
from utils.param_helper import ParamHelper
from utils.edg_relations import EdgArg, EdgRelation, EdgRelations
import glob
from collections import defaultdict
import re
from pymongo import MongoClient

rels_to_print = set(["inv", "reg", "ass", "cmp", "cov"])

columns = ("doc_id", "sent_index", "relation_id", "relation", "trigger", "trigger_offset",\
           "arg_num", "arg_head", "arg_head_offset", "arg_base_np", "arg_base_np_offset",\
           "arg_np", "arg_np_offset", "sent_text")
print("\t".join(columns))


def split_edge_name(edge_name):
    if re.search(r'arg[0-9]+_',edge_name):
        tokens = edge_name.split("_")
        rel_name = tokens[1]
        arg_number = tokens[0]
        if rel_name in rels_to_print:
            return (rel_name, arg_number)
        else:
            return (None,None)
    else:
        return (None,None)

def process_trigger(trigger, arg0, arg1):
    if trigger.lower().endswith("ing"):
        if any(term.lower() in arg0.lower() for term in arg1.split()):
            arg0 = arg0.split(trigger, 1)[0].strip()
            arg1 = arg1.replace(trigger, "").strip()
        if any(term.lower() in arg1.lower() for term in arg0.split()):
            arg1 = arg1.split(trigger, 1)[0].strip()
            arg0 = arg0.replace(trigger, "").strip()
    return arg0, arg1


def get_offset(proto_obj, doc):
    if type(proto_obj) == document_pb2.Sentence.Constituent:
        token_start = doc.token[proto_obj.token_start]
        token_end = doc.token[proto_obj.token_end]
        char_start = token_start.char_start
        char_end = token_end.char_end
        return  str(char_start)+":"+str(char_end)
    else:
        return str(proto_obj.char_start)+":"+str(proto_obj.char_end)

def load_regex_patterns(file_path):
    patterns = []
    with open(file_path, 'r') as file:
        for line in file:
            parts = line.strip().rsplit(',', 1)  # Split only on the last comma
            if len(parts) == 2:
                pattern, cls = parts
                patterns.append((re.compile(pattern, re.IGNORECASE), cls))
            else:
                print("Invalid line in regex file: {}".format(line))
    return patterns



def match_regex(term, regex_patterns):
    for pattern, cls in regex_patterns:
        match = pattern.search(term)
        if match:
            return match.group(), cls  
    return None, None

def match_terms(arg, dictionary):
    matched_terms = []
    matched_types = []
    matched_coids = []
    #dictionary_matched = False

    # Sort dictionary terms by length in descending order to prioritize longer matches
    sorted_terms = sorted(dictionary.keys(), key=len, reverse=True)

    for term in sorted_terms:
        entry = dictionary[term]

        # If the term is uppercase, match exactly; otherwise, ignore case
        if term.isupper():
            pattern = re.compile(r'\b' + re.escape(term) + r'\b')
        else:
            pattern = re.compile(r'\b' + re.escape(term) + r'\b', re.IGNORECASE)

        # If a match is found and it's not already part of a longer matched term, 
        # add the term and its types to the respective lists
        if pattern.search(arg) and not any([t for t in matched_terms if term in t]):
            matched_terms.append(term)
            matched_types.append(entry[0])
            matched_coids.append(entry[1])
            #dictionary_matched = True

    '''
    if not dictionary_matched:
        regex_term, regex_class = match_regex(arg, regex_patterns)
        if regex_class:
            matched_terms.append(regex_term)  # Use the actual matched term
            matched_types.append(regex_class)
    '''     

    return matched_terms, matched_types, matched_coids




def print_edg_relations(edg_relations, doc, dictionary):
    relation_id = 0
    helper = DocHelper(doc)
    sentences = doc.sentence
    results = []
    for trigger_rel, args in edg_relations.items():
        sent_index, relation, trigger_index = trigger_rel
        trigger = doc.token[trigger_index]
        trigger_offset = get_offset(trigger, doc)
        sentence = sentences[sent_index]
        arg0_list = []
        arg1_list = []
        arg0_head = []
        arg1_head = []
        arg0_base = []
        arg1_base = []

        for arg in args:
            arg_num, arg_head_index = arg
            arg_head = doc.token[arg_head_index]
            np_cst_index = helper.getParentNPIndexFromLeafTokenIndex(sentence,arg_head_index)
            base_np_cst_index = helper.getParentNPIndexFromLeafTokenIndex1(sentence,arg_head_index)
            np_cst = sentence.constituent[np_cst_index]
            base_np_cst = sentence.constituent[base_np_cst_index]

            base_noun_phrase = re.sub("\n"," ",helper.text(base_np_cst))
            full_noun_phrase = re.sub("\n"," ",helper.text(np_cst))
            sentence_text = re.sub("\n"," ",helper.text(sentence))
            

            to_print = (doc.doc_id, str(sent_index), str(relation_id), relation, trigger.word, trigger_offset,\
                        arg_num, arg_head.word, get_offset(arg_head, doc) , base_noun_phrase,\
                        get_offset(base_np_cst, doc), full_noun_phrase, get_offset(np_cst, doc), sentence_text)
            print ("\t".join(to_print))

            if arg_num == "arg0":
                arg0_list.append(helper.text(np_cst))
                arg0_head.append(arg_head.word)
                arg0_base.append(helper.text(base_np_cst))
            elif arg_num == "arg1":
                arg1_list.append(helper.text(np_cst))
                arg1_head.append(arg_head.word)
                arg1_base.append(helper.text(base_np_cst))
            
        if arg0_list and arg1_list:
            for i, arg0 in enumerate(arg0_list):

                for j, arg1 in enumerate(arg1_list):
                    arg0, arg1 = process_trigger(trigger.word, arg0, arg1)
                    arg0_matched, arg0_class, arg0_coids = match_terms(arg0, dictionary)
                    #print(arg0_class, arg0_coids)
                    arg1_matched, arg1_class, arg1_coids = match_terms(arg1, dictionary)

                    result = {
                        "PMID": doc.doc_id,
                        "trigger": trigger.word,
                        "arg0_np": arg0,
                        "arg0_head": arg0_head[i],
                        "arg0_base": arg0_base[i],
                        "arg0_matched": ', '.join(arg0_matched) if arg0_matched else None,
                        "arg0_type": ', '.join(arg0_class) if arg0_class else None,
                        "arg0_coid": ', '.join(arg0_coids) if arg0_coids else None,
                        "arg1_np": arg1,
                        "arg1_head": arg1_head[j],
                        "arg1_base": arg1_base[j],
                        "arg1_matched": ', '.join(arg1_matched) if arg1_matched else None,
                        "arg1_type": ', '.join(arg1_class) if arg1_class else None,
                        "arg1_coid": ', '.join(arg1_coids) if arg1_coids else None,
                        "sent_text": helper.text(sentence)
                    }
                    results.append(result)
        elif arg0_list:
            for i, arg0 in enumerate(arg0_list):
                arg0_matched, arg0_class = match_terms(arg0, dictionary)

                result = {
                    "PMID": doc.doc_id,
                    "trigger": trigger.word,
                    "arg0_np": arg0,
                    "arg0_head": arg0_head[i],
                    "arg0_base": arg0_base[i],
                    "arg0_matched": ', '.join(arg0_matched) if arg0_matched else None,
                    "arg0_type": ', '.join(arg0_class) if arg0_class else None,
                    "arg0_coid": ', '.join(arg0_coids) if arg0_coids else None,
                    "arg1_np": "",
                    "arg1_head": "",
                    "arg1_base": "",
                    "arg1_matched": 0,
                    "arg1_type": 0,
                    "arg1_coid": 0,
                    "sent_text": helper.text(sentence)
                }
                results.append(result)
        elif arg1_list:
            for i, arg1 in enumerate(arg1_list):
                arg1_matched, arg1_class = match_terms(arg1, dictionary)

                result = {
                    "PMID": doc.doc_id,
                    "trigger": trigger.word,
                    "arg0_np": "",
                    "arg0_head": "",
                    "arg0_base": "",
                    "arg0_matched": 0,
                    "arg0_type": 0,
                    "arg0_coid": 0,
                    "arg1_np": arg1,
                    "arg1_head": arg1_head[j],
                    "arg1_base": arg1_base[j],
                    "arg1_matched": ', '.join(arg1_matched) if arg1_matched else None,
                    "arg1_type": ', '.join(arg1_class) if arg1_class else None,
                    "arg1_coid": ', '.join(arg1_coids) if arg1_coids else None,
                    "sent_text": helper.text(sentence)
                }
                results.append(result)
        relation_id+=1
    
    return results

def merge_same_trigger(doc):
    helper = DocHelper(doc)
    trigger_to_arg = defaultdict(set)
    sentences = doc.sentence
    for sent in sentences:
        sent_index = sent.index
        for dep in sent.dependency_extra:
            trigger = dep.gov_index
            arg = dep.dep_index
            edge_name = dep.relation
            relation, arg_num = split_edge_name(edge_name)
            if relation:
                trigger_to_arg[(sent_index, relation, trigger)].add((arg_num, arg))

    return trigger_to_arg

def is_blacklisted(arg0_head, arg1_head, blacklist_words):
    # Split the head strings into words
    arg0_head_words = arg0_head.split()
    arg1_head_words = arg1_head.split()

    # Check if all the words in arg0_head or arg1_head are in the blacklist
    return all(word.lower() in blacklist_words for word in arg0_head_words) or \
           all(word.lower() in blacklist_words for word in arg1_head_words)

def run():

    #####Iterate through all files in Input directory and create doc_list
    input_dir_path = sys.argv[1]
    glob_path = input_dir_path + "/*.txt";
    input_files = glob.glob(glob_path)
    document_list = list()
    dictionary_file = "/home/shovan/nlputils/EDG_framework/Lexical_Concepts/transformed_data.json"  
    with open(dictionary_file, "r") as file:
        dictionary = json.load(file)
    
    #regex_patterns = load_regex_patterns('/home/shovan/nlputils/EDG_framework/Waters/Dictionary/regex_patterns.txt')
    

    for input_file in input_files:
        textFH = open(input_file,"r")
        text = textFH.read()
        textFH.close()
        raw_doc = document_pb2.Document()
        doc_id = os.path.splitext(os.path.basename(input_file))[0]
        raw_doc.text = text
        raw_doc.doc_id = doc_id 
        document_list.append(raw_doc)
        
    
    rule_phase0_filename = sys.argv[2]
    fh0 = open(rule_phase0_filename, "r")
    rule0_lines = fh0.readlines()
    fh0.close()

    ####NEED TO UPDDATE PARAM_HELPER
    param_helper = ParamHelper("NA","NA",rule0_lines,[],[])
    edg_rules = edgRules_pb2.EdgRules()

    param_helper.setRuleProtoAttributes(edg_rules)
    #param_helper.setDocProtoAttributes(raw_doc)
    # This is a simple function to make requests out of a list of documents. We
    # put 5 documents in each request.
    n = 2
    doc_index = 0
    documents_cnt = len(document_list)

    #blacklist words    
    blacklist_words = {"it", "its", "we", "model", "each", "%", "models", "result", "results", "approach", "approaches", "workflow", "workflows", "accurate", "automation", "method", "methods", "they", "which", "this", "their", "science", "us"}


    all_results = pd.DataFrame(columns=["PMID", "trigger", "arg0_np", "arg0_head", "arg0_base", "arg0_matched", "arg0_type", "arg0_coid", "arg1_np", "arg1_head", "arg1_base", "arg1_matched", "arg1_type", "arg1_coid", "sent_text"])
    blacklisted_results = pd.DataFrame(columns=all_results.columns)

    while doc_index < documents_cnt:
        end = documents_cnt if doc_index+n > documents_cnt else doc_index+n
        sublist = document_list[doc_index:end]
        requests = edg_request_iter_docs(sublist, edg_rules,
                                    request_size=5,
                                    request_type=rpc_pb2.EdgRequest.PARSE_BLLIP)

        # Given a request iterator, send requests in parallel and get responses.
        responses_queue = grpcapi.get_queue(server='127.0.0.1',
                                            port=8900,
                                            request_thread_num=10,
                                            iterable_request=requests,
                                            edg_request_processor=True)
        # Change the port number to the NLPServer port
        count = 0
        #result_list = []
        for response in responses_queue:
            for doc in response.document:
                helper = DocHelper(doc)
                sentences = doc.sentence
                doc_id = doc.doc_id
                edg_relations = merge_same_trigger(doc)
                results = print_edg_relations(edg_relations, doc, dictionary)
                for result in results:
                    arg0_h = result["arg0_head"]
                    arg1_h = result["arg1_head"]
                    result_row = pd.Series(result)
                    if is_blacklisted(arg0_h, arg1_h, blacklist_words):
                        blacklisted_results = blacklisted_results.append(result_row, ignore_index=True)
                    else:
                        all_results = all_results.append(result_row, ignore_index=True)
                count += 1
        
        doc_index = end

    
    all_results.to_excel("/home/shovan/nlputils/EDG_framework/Lexical_Concepts/test2.xlsx", index=False)
    blacklisted_results.to_excel("/home/shovan/nlputils/EDG_framework/Lexical_Concepts/blacklist_test2.xlsx", index=False)
    

if __name__ == '__main__':
    run()