
# coding: utf-8

import hashlib
import operator
import glob
import os
import re
from os import walk
from  __builtin__ import any as b_any
from numpy import array
from sklearn import tree
from sklearn.model_selection import cross_val_score
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn import svm, datasets
from sklearn.naive_bayes import GaussianNB
from sklearn.neighbors import KNeighborsClassifier
from sklearn import linear_model
from sklearn.model_selection import cross_val_predict
from sklearn.metrics import confusion_matrix
from sklearn.metrics import classification_report


def find_person(input):
    return  (re.finditer("<person>(.*?)</person>", input))


def get_features(name, line, start, end):
    feature_list = []
    f1 = feature_1_name_with_apostrophe(name, line, start, end)
    f2 = feature_2_prefix_strong(name,line,start,end)
    f3 = feature_3_prefix_new_line(name,line,start,end)
    #if the word is starting with new line, then there will be no prefix
    if f3:
        f4 = 0
    else:
        f4 = feature_4_prefix_medium(name,line,start,end)
    #if the word is starting with new line, then there will be no prefix
    if f3:
        f5 = 0
        f20 = 0
    else:
        f5,f20 = feature_5_prefix_strong(name,line,start,end)
        
    f6 = feature_6_suffix_with_character(name, line, start, end)
    #if the sentence or name has started off with the "." or "," then there would be no prefixes
    if f6 == 1:
        f7 = 0
        f21 = 0
    else:
        f7,f21 = feature_7_suffix_with_strong_words(name, line, start, end)
    #if the sentence or name has started off with the "." or "," then there would be no prefixes
    if f6 == 1:
        f8 = 0
    else:
        f8 = feature_8_suffix_with_strong_words(name,line,start,end)
    #words containing the the exhaustise list initialized in the below function should all be negative examples
    #if prime minister is included then it will return true for negative examples
    
    # Mr David Blunkett...following feature will help us in labelling , name = David as input as negative..
    #we wnt Full name to be identified
    if f6 == 1:
        f10 = 0
    else:
        f10 = feature_10_words_with_exhaustive_list(name,line,start,end)
    
    f11 = feature_11_words_with_exhaustive_list(name,line,start,end)
    f9 = feature_9_words_with_exhaustive_list(name,line,start,end)
    f12 = feature_12_word_length(name,line,start,end)
    f13 = feature_13_word_with_non_capital_prefix_suffix(name,line,start,end)
    
    #Note : F9 is skipped intentionally ---- moved to pre processing step

    
    feature_list = [f1,f2,f3,f4,f5,f6,f7,f8,f9,f10,f11,f12,f13]
    return feature_list


def feature_12_word_length(name,line,start,end):
    return len(name.split())


    
#check if the 's or s' is present at the end of the string      
def feature_1_name_with_apostrophe(name, line, start, end):
    
    suffix = name[-2:]
    
    if suffix == "'s" or suffix == "s'":
        return 1
    else:
        return 0
    
#check if word is the start of the sentence.
def feature_2_prefix_strong(string,line,start,end):
    index = start
    while line[index-1] == " ":
        index = index - 1
    if line[index-1] == "." or line[index-1] == "," or line[index-1] == "\"":
        return 1
    else:
        return 0
    

    
#check if the word is the start of the new line
def feature_3_prefix_new_line(name,line,start,end):
    index = start
    #this code directly picks up the new line if present
    if line[index-1] == "\n":
        return 1
    else:
        return 0
    
    #go back until you dont find capitalized word
    #return check_new_line(name,line,start,end)
    

#check if the given prefixes are present
def feature_4_prefix_medium(name,line,start,end):
    #identified prefix list
    prefix_word_list = ['and','said','leader','prime minister','justice','chairman','secretary','chancellor','reporter','journalist',
               'pm','president','mp','spokesperson','reporter','candidate']
    index = start
    while line[index-1] == " ":
        index = index - 1
    end_index = index
    #go back until you find the word
    while True:
        if line[index-1] == " " or line[index-1] == "\n":
            break
        else:
            index = index -1
            
            
    prefix = line[index:end_index].lower()
    if prefix in prefix_word_list:
        return 1
    else:
        return 0
#check if the given suffixes are present
def feature_5_prefix_strong(name,line,start,end):
    
    prefix_word_list = ['mr','ms','mrs','dr','lord','sir','lady','prince','minister','director','president','spokesman','spokeswoman']
    index = start
    while line[index-1] == " ":
        index = index - 1
    end_index = index
    #go back until you find the word
    while True:
        if line[index-1] == " " or line[index-1] == "\n":
            break
        else:
            index = index -1
       
    prefix = line[index:end_index].lower()
    if prefix in prefix_word_list:
        return 1,int(hashlib.md5(prefix).hexdigest()[:8], 16)
    else:
        return 0,int(hashlib.md5(prefix).hexdigest()[:8], 16)
    

#check if the word ends with comma or full stop
def feature_6_suffix_with_character(name,line,start,end):
    suffix = line[end:end+1]

    
    if suffix.isalpha():
        return 0
    else:
        return 1
    
    
#f7 should not be called ,if a check on the comma and full stop has become true    
#check if the suffixes are as given in the list
def feature_7_suffix_with_strong_words(name, line, start, end):
    character_count = len(line)
    suffix__word_list = ['said','told','claimed','mp','spokesman','spokesperson','spokeswoman','sr','jr','and','-','has','had']
    word_start = end+1
    index = word_start

    
    while index+1 < character_count:
            #print line[]
            if line[index+1] == '.' or line[index+1] == ',' or line[index+1] == " " or line[index+1] == "(" or line[index+1] == ")" or line[index+1] == "!":
                break
            else:
                index = index+1
            
    suffix = line[word_start:index+1]
    
    if suffix in suffix__word_list:
        return 1,int(hashlib.md5(suffix).hexdigest()[:8], 16)
    else:
        return 0,int(hashlib.md5(suffix).hexdigest()[:8], 16)
    
#check if the suffixes are as given in the list
def feature_8_suffix_with_strong_words(name, line, start, end):
    suffix__word_list = ['is','and']
    character_count = len(line)
    word_start = end+1
    index = word_start

    while index+1 < character_count:
        if line[index+1] == '.' or line[index+1] == ',' or line[index+1] == " " or line[index+1] == "(" or line[index+1] == ")" or line[index+1] == ")":
            break
        else:
            index = index+1
    suffix = line[word_start:index+1]
    
    if suffix in suffix__word_list:
        return 1
    else:
        return 0

#if these words are present make them as negative feature
def feature_9_words_with_exhaustive_list(name,line,start,end):
    lst = ['mr','mrs','ms','lord','leader','prime minister','justice','chairman','secretary','chancellor','reporter','journalist',
               'pm','minister','president','mp','spokesman','spokesperson','spokeswoman',
           'sir','lady','sr','jr','reporter','prince']
    
    name_list_split = name.split()
    
    name_list_split_new = [x.lower() for x in name_list_split]
    
    result = [val for val in name_list_split_new if val in lst]
    
    if len(result) >= 1:
        return 1
    else:
        return 0
 
#if the prefix contains these words and suffix is capitalized word then it is a feature for negative sample   
def feature_10_words_with_exhaustive_list(name,line,start,end):
    prefix_word_list = ['mr','ms','mrs','dr']
    character_count = len(line)
    #prefix fetch start
    index = start
    while line[index-1] == " ":
        index = index - 1
    end_index = index
    
    #go back until you find the word
    while index+1 < character_count:
        if line[index-1] == " " or line[index-1] == "\n":
            break
        else:
            index = index -1
       
   #prefix fetch end
    prefix = line[index:end_index].lower()
    
    #suffix fetch start
    word_start = end+1
    index = word_start
    
    #print line[word_start:word_start+3]

    if line[index] == "." or line[index] == ",":
        return 0
    while index+1 < character_count:
        if line[index+1] == '.' or line[index+1] == ',' or line[index+1] == " "  or line[index+1] == "(" or line[index+1] == ")":
            break
        else:
            index = index+1
    suffix = line[word_start:index+1]
    #suffix fetch end
    
    if prefix in prefix_word_list and bool(re.match(r'[A-Z][a-z]*', suffix)):
        return 1
    else:
        return 0

#if the prefix starts with small letter and suffix starts with small letter, it is a feature for positive sample
def feature_13_word_with_non_capital_prefix_suffix(name,line,start,end):
    #prefix fetch start
    character_count = len(line)
    index = start
    while line[index-1] == " ":
        index = index - 1
    end_index = index

    #go back until you find the word
    while index+1 < character_count:
        if line[index-1] == " " or line[index-1] == "\n":
            break
        else:
            index = index -1
       
    #prefix fetch end
    prefix = line[index:end_index].lower()

    #suffix fetch start
    word_start = end+1
    index = word_start

    #print line[word_start:word_start+3]

    while index+1 < character_count:
        if line[index+1] == '.' or line[index+1] == ',' or line[index+1] == " "  or line[index+1] == "(" or line[index+1] == ")":
            break
        else:
            index = index+1
    suffix = line[word_start:index+1]
    #suffix fetch end

    if bool(re.match(r'[a-z]+', prefix)) and bool(re.match(r'[a-z]+', suffix)):
        return 1
    else:
        return 0

    

#this feature checks if the word has a salutation - it is considered as a strong feature
def feature_11_words_with_exhaustive_list(name,line,start,end):
    prefix_word_list = ['mr','ms','mrs','dr']
    #prefix fetch start
    index = start
    while line[index-1] == " ":
        index = index - 1
    end_index = index
    
    #go back until you find the word
    while True:
        if line[index-1] == " " or line[index-1] == "\n":
            break
        else:
            index = index -1
       
   #prefix fetch end
    #dont convert to lower case as the exact match is required.
    prefix = line[index:end_index]
    
    if bool(re.match(r'[A-Z][a-z]*', prefix)):
        if prefix not in prefix_word_list:
            return 1
    return 0
        
    
    
#######################################################################
#######################################################################
#######################################################################

def remove_tags(input):
    input = re.sub('<person>',"",input)
    input = re.sub('</person>',"",input)
    return input


#negative sample generator
def generate_candidates(line, stop_word_list):
    actual_names_with_iter = find_person(line)
    actual_names_without_iter = []
    
    for item in actual_names_with_iter:
        actual_names_without_iter.append((re.sub('</person>',"",re.sub('<person>',"",line[item.start():item.end()]))).lower())
    line = remove_tags(line)
    
    candidates = set(re.finditer("[A-Z][a-zA-Z']*", line))
    candidates.update(re.finditer("[A-Z][a-zA-Z']* [A-Z][a-zA-Z']*", line))
    negative_candidates = []

    
    
    
    for item in candidates:
        name = line[item.start():item.end()].lower()
        
     
            
        if name not in actual_names_without_iter and name not in stop_word_list:
            split_names = name.split()
            result = [x for x in split_names if x in stop_word_list]
            if len(result) == 0:
                negative_candidates.append(item)
        
    
    return negative_candidates
    
        

    

positive = 0
negative = 0
  
def parse_file_and_get_features(filename,stop_word_list):

    with open(filename) as f:
        lines = f.readlines()

    features = []
    labels = []
    features_for_positive = []
    features_for_negative_set = []
    z = []
    i = 0
    
    
    ###########################---Code to Generate the Positive Set ---- ####################
    for line in lines:
        i=i+1
        if i > 1:
    #fetch the name of all people in the list
            person_list = find_person(line)
            if person_list is not None:
                for item in person_list:
                    name = line[item.start()+8:item.end()-9]
                    features_for_positive = get_features(name, line, item.start(), item.end())
                    features.append(features_for_positive)
                    labels.append(1)
                    z.append(tuple((name,features_for_positive,1)))
    
    global positive
    positive = positive + len(labels)
    #######################################################################################
    
    i = 0
    ###########################---Code to Generate the Negative Set ---- ####################
    for line in lines:
        i = i + 1
        if i > 1:
            if "<person>" in line and "</person>" in line:
                negative_candidates_list = generate_candidates(line, stop_word_list)
                line = remove_tags(line)
                #once all the negative candidates are generated need to take out the tags.
                #Note : Tags were already removed when we obtain the candidates therefore the the negative candidates positions
                #are wrt to original document
                for item in negative_candidates_list:
                    name = line[item.start():item.end()]

                    features_for_negative_set = get_features(name, line, item.start(),item.end())
                    features.append(features_for_negative_set)
                    labels.append(0)
                    z.append(tuple((name,features_for_negative_set,0)))
    #######################################################################################
    global negative
    negative = negative + len(labels)

    return features,labels,z

def train_and_test():
    with open("stop_words.txt") as f:
        stop_word_list = f.read().splitlines() 
        
    features = []
    labels = []
    names = []
    #os.chdir("../")
    filenames = glob.glob("../I-FOLDER/*.txt")
    for fname in filenames:
        x,y,z = parse_file_and_get_features(fname,stop_word_list)
        features.extend(x)
        labels.extend(y)
        


        
    trainDataset = array(features)
    trainTarget = array(labels)

    cvs_scores = {}

    
    classifier = {'DecisionTree' : DecisionTreeClassifier(random_state=0,max_depth = 5)}


    
    features_test = []
    labels_test = []
    filenames = glob.glob("../J-FOLDER/*.txt")
    for fname in filenames:
        x,y,z = parse_file_and_get_features(fname,stop_word_list)
        features_test.extend(x)
        labels_test.extend(y)
        names.extend(z)

    

    testDataset = array(features_test)
    testTarget = array(labels_test)

    for clssfr in classifier:
        clf = classifier[clssfr]
        clf = clf.fit(trainDataset, trainTarget)
        y_pred = clf.predict(testDataset)
        print "classifier name" , clssfr
        print(classification_report(testTarget, y_pred))







def cross_validation():

    with open("stop_words.txt") as f:
        stop_word_list = f.read().splitlines() 


        
    features = []
    labels = []
    names = []
    

    filenames = glob.glob("../I-FOLDER/*.txt")
    for fname in filenames:
        x,y,z = parse_file_and_get_features(fname,stop_word_list)
        features.extend(x)
        labels.extend(y)
        names.extend(z)


        #MAIN FUNCTION##
    trainDataset = array(features)
    trainTarget = array(labels)

    cvs_scores = {}

    

    classifier = {'DecisionTree' : DecisionTreeClassifier(random_state=0,max_depth = 5) ,
    'SVM ' : svm.SVC(probability=True, random_state=0),
    'RandomForest' :    RandomForestClassifier(max_depth=2, random_state=0),
    'LogisticRegression' : linear_model.LogisticRegression(C=1e5) }
    
    
    for clf in classifier:
        precisionScores = cross_val_score(classifier[clf], trainDataset, trainTarget, cv=10, scoring='precision')
        recallScores = cross_val_score(classifier[clf], trainDataset, trainTarget, cv=10, scoring='recall')
        cvs_scores[clf] = { precisionScores.mean(), recallScores.mean()}

    # clf = RandomForestClassifier(max_depth=2, random_state=0)
    # y_pred = cross_val_predict(clf,trainDataset,trainTarget,cv=10)
    # conf_mat = confusion_matrix(trainTarget,y_pred)

    #precisionScores = cross_val_score(DecisionTreeClassifier(random_state=0,max_depth = 5), trainDataset, trainTarget, cv=5, scoring='precision')



    for val in cvs_scores:
        print val, " \t:\t", cvs_scores[val] 

    print "\n==================================== LinearRegression ===================================="
    linreg = linear_model.LinearRegression()
    linreg.fit(trainDataset, trainTarget)

    linpredict = linreg.predict(trainDataset)
    

    for jj in zip(range(len(linpredict))):
        if linpredict[jj] >= 0.5:
            linpredict[jj] = 1
        else:
            linpredict[jj] = 0

    print(classification_report(trainTarget, linpredict))





def main():

        #training phase - cross validation is done here
        cross_validation()

        #testing after the cross validation phase
        #train_and_test()
    

        
main()  





    
        
    

    

