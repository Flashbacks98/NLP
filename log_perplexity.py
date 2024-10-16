import math

def count_words(inputFile):
    # Initialize a dictionary to hold word counts
    words_dict = {}
    inputFile.seek(0)  # Ensure we're at the start of the file
    for line in inputFile:
        for word in line.split():  # Split the line into words
            lowerCaseWord = word.lower()  # Convert word to lowercase
            # Update word count in the dictionary
            if (lowerCaseWord not in words_dict):
                words_dict.update({lowerCaseWord: 1})  # Add new word with count 1
            else:
                words_dict[lowerCaseWord] += 1  # Increment count for existing word
    return words_dict  # Return the dictionary of word counts

def unk_sentences(inputFile, outputFile, words_dict, removed_words):
    inputFile.seek(0)  # Ensure we're at the start of the file
    for line in inputFile:
        outputFile.write("<s> ")  # Write sentence start symbol
        for word in line.split():
            writtenWord = word.lower()  # Convert word to lowercase
            # Replace unique or banned words with <unk>
            if (writtenWord in words_dict) and (words_dict[writtenWord] == 1):
                writtenWord = "<unk>"
            elif writtenWord in removed_words:
                writtenWord = "<unk>"
            outputFile.write(writtenWord + " ")  # Write processed word
        outputFile.write("</s>\n")  # Write sentence end symbol

def compare_to(dict1, dict2):
    return [element for element in dict1 if element not in dict2]

def unigram_model(words_dict, totalWords):
    # Create a unigram model with probabilities
    unigram_model = {}
    for key in words_dict:
        probability = round(words_dict[key]/totalWords, 8)  # Calculate probability
        unigram_model.update({key: probability})  # Update model with probability
    return unigram_model  # Return the unigram model

def create_bigram(inputFile):
    # Create a bigram model from the input file
    bigram = {}
    inputFile.seek(0)  # Ensure we're at the start of the file
    for line in inputFile:
        words = line.split()  # Split line into words
        for i in range(0, len(words)):
            # Check if the bigram exists and update count accordingly
            if (i < len(words)-1) and (tuple([words[i], words[i+1]]) not in bigram): 
                bigram.update({tuple([words[i], words[i+1]]): 1})  # Add new bigram
            elif (i < len(words)-1):
                bigram[tuple([words[i], words[i+1]])] += 1  # Increment existing bigram count
    return bigram  # Return the bigram model

def bigram_model(bigram_dict, word_dict):
    # Create a bigram model with probabilities
    bigram_model = {}
    for key in bigram_dict:
        probability = round(bigram_dict[key]/word_dict[key[0]], 8)  # Calculate probability
        bigram_model.update({key: probability})  # Update model with probability
    return bigram_model  # Return the bigram model

def add_one_smoothing(bigram_dict, word_dict, uniqueWords):
    # Create a bigram model with Add-One smoothing
    add_one_smoothing = {}
    for key in bigram_dict:
        # Calculate probability with Add-One smoothing
        probability = round(((1.0 + bigram_dict[key]) / (uniqueWords + word_dict[key[0]])), 8)
        add_one_smoothing.update({key: probability})  # Update model with probability
    return add_one_smoothing  # Return the Add-One smoothed model

def writeDict(dict, outputFile):
    # Write dictionary contents to an output file
    for key in dict:
        outputFile.write("{" + str(key) + "}" + ": " + str(dict[key]) + "\n")  # Write key-value pairs
    outputFile.write("\n")  # Add a newline for separation

def process_sentence(sentence, words_dict):
    # Process a sentence, replacing unseen words with <unk>
    processed_sentence = "<s> "  # Start with sentence start symbol
    for word in sentence.split():
        if word.lower() not in words_dict:
            processed_sentence += "<unk> "  # Replace unseen word with <unk>
        else:
            processed_sentence += (word.lower() + " ")  # Add known word
    processed_sentence += " </s>"  # End with sentence end symbol
    return processed_sentence  # Return processed sentence

def calculate_unigram_log(sentence, unigram_model):
    # calculate log probabilities for the unigram model
    probability = 0
    for word in sentence.split():
        probability += math.log(unigram_model[word], 2)  # Accumulate log probabilities
    probability = round(probability, 4)  # Round to 4 decimal places
    return probability  # Return total log probability

def calculate_bigram_log(sentence, bigram_model, unigram_model):
    # calculate log probabilities for the bigram model
    probability = 0
    words = sentence.split()
    probability += math.log(unigram_model[words[0]], 2)  # Add log of first word probability
    for i in range(0, len(words) - 1):
        tuple_word = tuple([words[i], words[i+1]])
        if tuple_word in bigram_model:
            probability += math.log(bigram_model[tuple_word], 2)  # Add log of bigram probability
    probability = round(probability, 4)  # Round to 4 decimal places
    return probability  # Return total log probability

def calculate_add_one_smoothing_log(sentence, add_one_smoothing, unigram_model):
    # calculate log probabilities for the Add-One smoothing model
    probability = 0
    words = sentence.split()
    probability += math.log(unigram_model[words[0]], 2)  # Add log of first word probability
    for i in range(0, len(words) - 1):
        tuple_word = tuple([words[i], words[i+1]])
        if tuple_word in add_one_smoothing:
            probability += math.log(add_one_smoothing[tuple_word], 2)  # Add log of smoothed bigram probability
    probability = round(probability, 4)  # Round to 4 decimal places
    return probability  # Return total log probability

def calculate_perplexity(logModel, totalWords):
    # Calculate perplexity from log probability
    result = math.exp((-1.0 / totalWords) * logModel)  # calculate perplexity
    return round(result, 4)  # Return rounded perplexity

if __name__ == "__main__":
    # 1.1: Open files for processing
    testFile = open("test.txt", "r", errors="ignore")
    trainFile = open("train.txt", "r", errors="ignore")

    processedTestFile = open("processedTest.txt", "w")
    processedtrainFile = open("processedTrain.txt", "w")

    # Count words in the training file and banned words from the test file
    words_dict = count_words(trainFile)
    removed_words = compare_to(count_words(testFile), words_dict)

    # Process the test and training files
    unk_sentences(testFile, processedTestFile, words_dict, removed_words)
    unk_sentences(trainFile, processedtrainFile, words_dict, [])

    # Close the processed files
    processedtrainFile.close()
    processedTestFile.close()

    # 1.2: Open processed files for further analysis
    processedTestFile = open("processedTest.txt", "r")
    processedtrainFile = open("processedTrain.txt", "r")

    words_dict = count_words(processedtrainFile)  # Count words in processed training file

    # Calculate total token count
    totalTokenCount = 0
    for key in words_dict:
        totalTokenCount += words_dict[key]  # Accumulate total token count
    
    # Create models
    unigram_model = unigram_model(words_dict, totalTokenCount)
    bigram_dict = create_bigram(processedtrainFile)
    bigram_model = bigram_model(bigram_dict, words_dict)

    # Calculate unique tokens for Add-One smoothing
    uniqueTokens = 0
    for key in words_dict:
        uniqueTokens += 1  # Count unique tokens
    add_one_smoothing = add_one_smoothing(bigram_dict, words_dict, uniqueTokens)

    outputFile = open("1.2Answers.txt", "w")  # Open output file for results

    # Write models to output file
    outputFile.write("< A unigram maximum likelihood model >\n")
    writeDict(unigram_model, outputFile)
    outputFile.write("< A bigram maximum likelihood model >\n")
    writeDict(bigram_model, outputFile)
    outputFile.write("< A bigram model with Add-One smoothing >\n")
    writeDict(add_one_smoothing, outputFile)

    # 1.3
    # Question 5
    sentence = "I look forward to hearing your reply ."
    sentence = process_sentence(sentence, words_dict)  # Process the sample sentence
    unigram_log = calculate_unigram_log(sentence, unigram_model)  # Calculate unigram log probability
    bigram_log = calculate_bigram_log(sentence, bigram_model, unigram_model)  # Calculate bigram log probability
    add_one_log = calculate_add_one_smoothing_log(sentence, add_one_smoothing, unigram_model)  # Calculate smoothed log probability

    print(unigram_log)
    print(bigram_log)
    print(add_one_log)

    # Question 6: Calculate perplexity for each model
    total_sentence_words = 0
    for word in sentence.split():
        total_sentence_words += 1  # Count words in the sentence

    perplexity_unigram = calculate_perplexity(unigram_log, total_sentence_words)  # Calculate unigram perplexity
    perplexity_bigram = calculate_perplexity(bigram_log, total_sentence_words)  # Calculate bigram perplexity
    perplexity_add_one = calculate_perplexity(add_one_log, total_sentence_words)  # Calculate smoothed perplexity

    # Print perplexity results
    print(perplexity_unigram)
    print(perplexity_bigram)
    print(perplexity_add_one)

    # Close all open files
    outputFile.close()
    processedtrainFile.close()
    processedTestFile.close()
    trainFile.close()
    testFile.close()