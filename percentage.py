# Question 1.3.3

def build_vocabulary(inputFile):
    vocabulary = set()
    
    for line in inputFile: 
        words = line.strip().split()
        vocabulary.update([word for word in words if word != "<cs>"])

    return vocabulary

def calculate_percentage(testFile, vocabulary):
    total_tokens = 0
    oov_tokens = 0
    total_types = set()
    oov_types = set()

    for line in testFile:
        words = line.strip().split()
        # Ignore <cs> but include </s>
        words = [word for word in words if word != "<cs>"]

        for word in words:
            total_tokens += 1
            total_types.add(word)
            if word not in vocabulary:
                oov_tokens +=1 
                oov_types.add(word)
    
    token_oov_percentage = (oov_tokens / total_tokens) * 100
    type_oov_percentage = (len(oov_types) / len(total_types)) * 100

    return token_oov_percentage, type_oov_percentage



if __name__ == "__main__":
    testFile = open("test.txt", "r", errors="ignore")
    trainFile = open("train.txt", "r", errors="ignore")

    vocab = build_vocabulary(trainFile)
    token_oov_percentage, type_oov_percentage = calculate_percentage(testFile, vocab)

    print(f"OOV Token Percentage: {token_oov_percentage:.2f}%")
    print(f"OOV Type Percentage: {type_oov_percentage:.2f}%")

    processedTestFile = open("processedTest.txt", "w")
    processedTrainFile = open("processedTrain.txt", "w")

