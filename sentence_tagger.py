from collections import defaultdict

# 1.1.1 Pad sentences with <cs> and </cs>
"""
def pad_sentences(inputFile, outputFile): 
    for line in inputFile:
        outputFile.write("<cs> " + line.strip() + "</s>\n") # Pad <cs>, get rid of end whitespace, pad </cs> at end of each line
"""
# 1.1.2 Turn all characters lowercase
"""
def lowercase_sentences(inputFile, outputFile):
    for line in inputFile:
       outputFile.write("<cs> " + line.strip().lower() + "</s>\n") # Pad <cs>, get rid of end whitespace, pad </cs> at end of each line
"""
# 1.1.3 All characters that occur once in training become <unk>, and words in test that appear in training also become <unk>
def count_words(inputFile):
    unique_words = defaultdict(int)
    inputFile.seek(0)
    for line in inputFile:
        for word in line.split():
                unique_words[word.lower()] += 1
    return dict(unique_words)

def count_total_words(inputFile):
    total_words = 0
    inputFile.seek(0)  # Ensure you start reading from the beginning of the file
    for line in inputFile:
        total_words += len(line.split())
    return total_words

def compare_to(dict1, dict2):
    return [element for element in dict1 if element not in dict2]

def unk_sentences(inputFile, outputFile, unique_words, removedWords):
    inputFile.seek(0)
    for line in inputFile:
        outputFile.write("<cs> ")
        for word in line.split():
            writtenWord = word.lower()
            if unique_words.get(writtenWord, 0) == 1 or writtenWord in removedWords:
                writtenWord = "<unk>"
            outputFile.write(writtenWord + " ")
        outputFile.write("</s>\n")

# Main Function

if __name__ == "__main__":
    testFile = open("test.txt", "r", errors="ignore")
    trainFile = open("train.txt", "r", errors="ignore")

    processedTestFile = open("processedTest.txt", "w")
    processedTrainFile = open("processedTrain.txt", "w")

# Section 1.1 Function Calls

# 1.1.1
# pad_sentences(testFile, processedTestFile)
# pad_sentences(trainFile, processedTrainFile)

# 1.1.2
# lowercase_sentences(testFile, processedTestFile)
# lowercase_sentences(trainFile, processedTrainFile)

# 1.1.3
unique_words = count_words(trainFile)
removedWords = compare_to(count_words(testFile), unique_words)

unk_sentences(testFile, processedTestFile, unique_words, removedWords)
unk_sentences(trainFile, processedTrainFile, unique_words, [])

processedTestFile = open("processedTest.txt", "r", errors="ignore")
processedTrainFile = open("processedTrain.txt", "r", errors="ignore")

# 1.3.1
processed_word_counts = count_words(processedTrainFile)
print(processed_word_counts)

total_unique_words = len(processed_word_counts)

print(f"Total unique words: {total_unique_words}")

# 1.3.2

total_word_count = count_total_words(processedTrainFile)
print("Total word count in training corpus:", total_word_count)

testFile.close()
trainFile.close()
processedTestFile.close()
processedTrainFile.close()

    
    
