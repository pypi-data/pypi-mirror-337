Semantic Comparison Network (SCN or SCNet), is a new revolutionary artificial neural network architecture developed with a focus on creating language models and which uses the HurNet network as a calculation base.

# Semantic Comparison Network (SCN/SCNet)

This code was programmed, designed and developed by Ben-Hur Varriano for Sapiens Technology®️ and aims to create language models using a new network architecture that aims to increase speed, performance and efficiency in training and inference for natural language processing. The name of the proposed network is Semantic Comparison Network, also known as SCN or SCNet. This network works with semantic comparison and Euclidean distance calculations that function as an expansion of resources for the main calculation base of the HurNet network. Any change, adaptation and/or increase in the original code, as well as the distribution, public comment and/or sharing of the logic of this algorithm without prior authorization from Sapiens Technology®️ is strictly prohibited and if these rules are not followed, our legal team of lawyers will formally sue the executor.

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install the Semantic Comparison Network.

```bash
pip install semantic-comparison-network
```

## Usage
Basic usage example:
```python
from semantic_comparison_network import SemanticComparisonNetwork # import of the main class contained in the module
scnet = SemanticComparisonNetwork() # creation of a class instantiation variable that will be used to access the resources available within it
# use the "addFit" method to add a possible question with its respective answer to the model training
# the "prompt" parameter receives a string with the question and the "answer" parameter receives a string with the answer that will be returned when this question is asked
# you can call the "addFit" method as many times as you want to add as many input and output pairs as needed (there is no limit)
# here we are using only a single question for each answer, but we advise you to register multiple questions with the same meaning for the same answer, this way your model will be more accurate
scnet.addFit(prompt='What does the acronym GPT mean in language models?', answer='GPT in language models stands for Generative Pre-trained Transformer.')
scnet.addFit(prompt='What is the capital of Spain?', answer='The capital of Spain is Madrid.')
# use the "predict" function to perform model inference and return its prediction
# the "prompt" parameter receives a string with the question for which an answer is desired
# the "predict" function will return a string with one of the responses registered with the "addFit" method
# note that it is not necessary to use a question exactly the same as one of the registered questions, it just needs to be a semantically similar question
answer = scnet.predict(prompt='what does GPT mean in language models?') # returns the answer equivalent to the training question that is most semantically similar to the prediction question
print(answer) # displays the response found in model training

```
Prediction response:
```bash
GPT in language models stands for Generative Pre-trained Transformer.
```
```python
from semantic_comparison_network import SemanticComparisonNetwork
scnet = SemanticComparisonNetwork()

scnet.addFit(prompt='What does the acronym GPT mean in language models?', answer='GPT in language models stands for Generative Pre-trained Transformer.')
scnet.addFit(prompt='What is the capital of Spain?', answer='The capital of Spain is Madrid.')

answer = scnet.predict(prompt='what is the name of the capital of spain?')
print(answer)

```
Prediction response:
```bash
The capital of Spain is Madrid.
```

Use the "saveModel" method to save the current training.
```python
from semantic_comparison_network import SemanticComparisonNetwork
scnet = SemanticComparisonNetwork()

scnet.addFit(prompt='What does the acronym GPT mean in language models?', answer='GPT in language models stands for Generative Pre-trained Transformer.')
scnet.addFit(prompt='What is the capital of Spain?', answer='The capital of Spain is Madrid.')
# use the "saveModel" method to save a pre-trained model, so it will no longer be necessary to train it again in future predictions
# the model files will be saved in a example directory called "file_path" which will be created if it does not already exist and all files will have the name "model" (each with its respective extension)
# you can choose the directory you want to save, as well as use the name you want for the files that will be created in the directory (as an example we will be using the name "model" for the files)
# all files will have the same name, but with different extensions
# three files will be created: ".scconf" with the model settings, ".scnnet" or ".hurnet" with the model weights and ".vocabu" with the vocabulary of possible answers
model_path = './file_path/model' # variable with the path of the model that will be created (model is the name for the three files that will be generated)
scnet.saveModel(model_path=model_path) # saving method that receives in the parameter named "model_path" the path and name of the files that will be generated

```
```bash
Saving semantic model: 100%|████████████████████████████████████████████████████████████████████████████████████████████████████████████████████| 7/7 [00:00<00:00, 11886.69it/s]
```
Use the "loadModel" method to load a pre-trained model that is contained in any directory.
```python
from semantic_comparison_network import SemanticComparisonNetwork
scnet = SemanticComparisonNetwork()
# use the method named "loadModel" to load a pre-trained model that has already been saved previously
# by loading a pre-trained model, your prediction will be much faster because there will be no need for new training
# the "loadModel" method must receive in the parameter named "model_path" the same path that was used in the save
# "model_path" can receive the full path with the name of the weights file ".scnnet" or ".hurnet", or simply the path of the directory where the files are located
# if you want, you can share the pre-trained model on the internet so that it can be run on other machines without the need for re-training
model_path = './file_path/model' # it could also be "./file_path" or "file_path" and the result would be the same
scnet.loadModel(model_path=model_path) # pre-trained model loading method
# after the model has been loaded, simply make the prediction as normal
answer = scnet.predict(prompt='what is the name of the capital of spain?')
print(answer)

```
```bash
Loading semantic model: 100%|███████████████████████████████████████████████████████████████████████████████████████████████████████████████████| 7/7 [00:00<00:00, 15658.73it/s]
The capital of Spain is Madrid.
```
Check out another example of model loading below.
```python
from semantic_comparison_network import SemanticComparisonNetwork
scnet = SemanticComparisonNetwork()

model_path = './file_path/model.scnnet' # if you prefer, you can specify the extension of the weights file
scnet.loadModel(model_path=model_path, progress=False) # use the "progress" parameter equal to False if you want to disable the progress bar (default is True)

answer = scnet.predict(prompt='what is the name of the capital of spain?')
print(answer)

```
```bash
The capital of Spain is Madrid.
```
Below is another example of saving using the full name of the weights file.
```python
from semantic_comparison_network import SemanticComparisonNetwork
scnet = SemanticComparisonNetwork()

scnet.addFit(prompt='What does the acronym GPT mean in language models?', answer='GPT in language models stands for Generative Pre-trained Transformer.')
scnet.addFit(prompt='What is the capital of Spain?', answer='The capital of Spain is Madrid.')
# if you prefer, you can specify the weights file extension ".scnnet" for the default training method or ".hurnet" if you are using the hurnet training method
model_path = './file_path/model.scnnet' # specifies the path to the weights file that will be generated, the other files will be generated in the same directory automatically
scnet.saveModel(model_path=model_path, progress=False) # use "progress" equal to False if you want to hide the progress bar (default is True)

```
Note that if you prefer, you can specify just the path to the model directory and the library itself will take care of finding the necessary files in this directory.
```python
from semantic_comparison_network import SemanticComparisonNetwork
scnet = SemanticComparisonNetwork()

model_path = './file_path' # if you want, you can define only the path of the model folder, in this example the folder is in the local directory, but it could be in any directory
scnet.loadModel(model_path=model_path, progress=False)

answer = scnet.predict(prompt='what is the name of the capital of spain?')
print(answer)

```
```bash
The capital of Spain is Madrid.
```
Always register in your training as many variations as you can for the same question.
```python
from semantic_comparison_network import SemanticComparisonNetwork
scnet = SemanticComparisonNetwork()
# create multiple questions for the same answer, so your model will be more accurate and less prone to errors
# below we have created two questions for each answer, but you should create as many variations as you can
# do this by registering as many questions and answers about your area of study as possible
# be careful not to register questions and/or answers with spelling mistakes, otherwise your model may learn to write with incorrect spelling
# multiple questions for the same answer about the meaning of the acronym gpt
scnet.addFit(prompt='What does the acronym GPT mean in language models?', answer='GPT in language models stands for Generative Pre-trained Transformer.')
scnet.addFit(prompt='Tell me what is the meaning of GPT in language models.', answer='GPT in language models stands for Generative Pre-trained Transformer.')
# multiple questions for the same answer about the capital of spain
scnet.addFit(prompt='What is the capital of Spain?', answer='The capital of Spain is Madrid.')
scnet.addFit(prompt='Tell me the name of the capital of Spain.', answer='The capital of Spain is Madrid.')
# you can call the prediction function as many times as you want
answer = scnet.predict(prompt='i want to know what the capital of spain is')
print(answer) # response: The capital of Spain is Madrid.
answer = scnet.predict(prompt='i want to know what gpt means')
print(answer) # response: GPT in language models stands for Generative Pre-trained Transformer.

```
```bash
The capital of Spain is Madrid.
GPT in language models stands for Generative Pre-trained Transformer.
```
Use the method named "train" to insert all inputs and outputs into the model at once.
```python
from semantic_comparison_network import SemanticComparisonNetwork
scnet = SemanticComparisonNetwork()
# with the "string" parameter of the method named "train" it is possible to register unstructured inputs and outputs for model training (this is not recommended, only do it in cases where it is really necessary
string = '''
What does the acronym GPT mean in language models?
GPT in language models stands for Generative Pre-trained Transformer.

Tell me what is the meaning of GPT in language models.
GPT in language models stands for Generative Pre-trained Transformer.

What is the capital of Spain? The capital of Spain is Madrid.
Tell me the name of the capital of Spain. The capital of Spain is Madrid.
'''
scnet.train(string=string) # with the method named "train" it is possible to train a model in a single step without the need to register the question and answer pairs one by one

answer = scnet.predict(prompt='i want to know what the capital of spain is')
print(answer)

```
```bash
Converting text: 100%|████████████████████████████████████████████████████████████████████████████████████████████████████████████████████| 383/383 [00:00<00:00, 2942158.30it/s]
Structuring data: 100%|█████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████| 4/4 [00:00<00:00, 41630.81it/s]
Semantic model training: 100%|█████████████████████████████████████████████████████████████████████████████████████████████████████████████████████| 7/7 [00:00<00:00, 83.15it/s]
Tokenizing data: 100%|█████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████| 4/4 [00:00<00:00, 47.79it/s]
The capital of Spain is Madrid.
```
To disable single-step training progress, use the "progress" parameter set to False.
```python
from semantic_comparison_network import SemanticComparisonNetwork
scnet = SemanticComparisonNetwork()
# always keep the content with the question first and the answer after
# note: avoid leaving the content unstructured in this way, place all the answers to the right of their respective questions or all the answers below their respective questions
string = '''
What does the acronym GPT mean in language models? GPT in language models stands for Generative Pre-trained Transformer.
Tell me what is the meaning of GPT in language models.
GPT in language models stands for Generative Pre-trained Transformer.
What is the capital of Spain? The capital of Spain is Madrid.
Tell me the name of the capital of Spain.
The capital of Spain is Madrid.
'''
scnet.train(string=string, progress=False) # with the "progress" parameter equal to False it is possible to disable training progress (the default is True)

scnet.saveModel(model_path='./model_directory/my_model', progress=False)
# check the files generated in the path "./model_directory"

```
```python
from semantic_comparison_network import SemanticComparisonNetwork
scnet = SemanticComparisonNetwork()

scnet.loadModel(model_path='model_directory', progress=False)

print(scnet.predict(prompt='What does the acronym GPT mean in language models?'))
print(scnet.predict(prompt='Tell me what is the meaning of GPT in language models.'))
print(scnet.predict(prompt='What is the capital of Spain?'))
print(scnet.predict(prompt='Tell me the name of the capital of Spain.'))

```
```bash
GPT in language models stands for Generative Pre-trained Transformer.
GPT in language models stands for Generative Pre-trained Transformer.
The capital of Spain is Madrid.
The capital of Spain is Madrid.
```
Example of training a model with the HurNet network architecture.
```python
from semantic_comparison_network import SemanticComparisonNetwork
scnet = SemanticComparisonNetwork()
# preferably organize the input and output pairs with the outputs below the inputs and with a blank line between the pairs
string = '''
What does the acronym GPT mean in language models?
GPT in language models stands for Generative Pre-trained Transformer.

Tell me what is the meaning of GPT in language models.
GPT in language models stands for Generative Pre-trained Transformer.

What is the capital of Spain?
The capital of Spain is Madrid.

Tell me the name of the capital of Spain.
The capital of Spain is Madrid.
'''
scnet.train(string=string, method='hurnet', progress=True)
# note that when using the 'hurnet' training method, you can optionally explicitly specify the hurnet extension for the main file
scnet.saveModel(model_path='./hurnet_model/my_model.hurnet', progress=True)

```
```bash
Converting text: 100%|████████████████████████████████████████████████████████████████████████████████████████████████████████████████████| 384/384 [00:00<00:00, 2977103.02it/s]
Structuring data: 100%|█████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████| 4/4 [00:00<00:00, 39199.10it/s]
Hurnet model training: 100%|███████████████████████████████████████████████████████████████████████████████████████████████████████████████████████| 7/7 [00:00<00:00, 83.23it/s]
Tokenizing data: 100%|█████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████| 4/4 [00:00<00:00, 47.85it/s]
Saving hurnet model: 100%|██████████████████████████████████████████████████████████████████████████████████████████████████████████████████████| 7/7 [00:00<00:00, 17497.10it/s]
```
You can also optionally specify the main file extension explicitly when uploading.
```python
from semantic_comparison_network import SemanticComparisonNetwork
scnet = SemanticComparisonNetwork()
# the .hurnet extension is optional when loading and can therefore be hidden if you prefer
scnet.loadModel(model_path='./hurnet_model/my_model.hurnet', progress=True)

print(scnet.predict(prompt='What is the capital of Spain?'))
print(scnet.predict(prompt='Tell me the name of the capital of Spain.'))

```
```bash
Loading semantic model: 100%|████████████████████████████████████████████████████████████████████████████████████████████████████████████████████| 7/7 [00:00<00:00, 5907.47it/s]
The capital of Spain is Madrid.
The capital of Spain is Madrid.
```
You can also choose not to use any custom name for your template, in which case it will be saved with a default name.
```python
from semantic_comparison_network import SemanticComparisonNetwork
scnet = SemanticComparisonNetwork()
# you can also place the input and output pairs one below the other with no blank line between them, but this is not recommended
string = '''
What does the acronym GPT mean in language models?
GPT in language models stands for Generative Pre-trained Transformer.
Tell me what is the meaning of GPT in language models.
GPT in language models stands for Generative Pre-trained Transformer.
What is the capital of Spain?
The capital of Spain is Madrid.
Tell me the name of the capital of Spain.
The capital of Spain is Madrid.
'''
scnet.train(string=string, progress=True)
scnet.saveModel() # it is also possible to save the model without assigning any saving parameters, in this case the model will be saved with a default name in the root directory

```
```bash
Converting text: 100%|████████████████████████████████████████████████████████████████████████████████████████████████████████████████████| 381/381 [00:00<00:00, 3003815.46it/s]
Structuring data: 100%|█████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████| 4/4 [00:00<00:00, 39662.45it/s]
Semantic model training: 100%|█████████████████████████████████████████████████████████████████████████████████████████████████████████████████████| 7/7 [00:00<00:00, 83.32it/s]
Tokenizing data: 100%|█████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████| 4/4 [00:00<00:00, 47.88it/s]
Saving semantic model: 100%|████████████████████████████████████████████████████████████████████████████████████████████████████████████████████| 7/7 [00:00<00:00, 16951.58it/s]
```
If no model is referenced in the load method, it will look for a model with the default name in the root directory.
```python
from semantic_comparison_network import SemanticComparisonNetwork
scnet = SemanticComparisonNetwork()
scnet.loadModel()
print(scnet.predict(prompt='What is the capital of Spain?'))
print(scnet.predict(prompt='Tell me the name of the capital of Spain.'))

```
```bash
Loading semantic model: 100%|███████████████████████████████████████████████████████████████████████████████████████████████████████████████████| 7/7 [00:00<00:00, 12520.31it/s]
The capital of Spain is Madrid.
The capital of Spain is Madrid.
```
The most appropriate way to train language models is through a structured JSON file with questions and answers. This way, your training will be much more accurate and the answers will be much more precise.
Example JSON (dataset.json):
```json
{
	"data": [
				{
					"input": "Hello! Who are you?",
					"output": "Hello! I am Sapiens Chat, an AI model created by Sapiens Technology."
				},
				{
					"input": "Who discovered Brazil?",
					"output": "Brazil was discovered by Portuguese navigators led by Pedro Álvares Cabral in 1500."
				},
				{
					"input": "What is the main language spoken in Spain?",
					"output": "The main language spoken in Spain is Spanish."
				},
				{
					"input": "What is the capital of Portugal?",
					"output": "The capital of Portugal is Lisbon."
				},
				{
					"input": "How much is 2 + 2?",
					"output": "The sum of 2 + 2 in mathematics is 4."
				},
				{
					"input": "What is five minus three?",
					"output": "The result of five minus three is two."
				},
				{
					"input": "What is your name?",
					"output": "My name is Sapiens Chat."
				}
	]
}
```
```python
from semantic_comparison_network import SemanticComparisonNetwork
scnet = SemanticComparisonNetwork()
# it is highly recommended that you use a properly formatted json file to train your model
# the json file must have a key in array format named "data" to represent a list of records
# the array of the key "data" must have one or more elements in json format to represent the data dictionaries
# each json in the "data" array must contain a key named "input" for registering the question and a key named "output" for registering the answer
# the json file must have the following format: {"data": [{"input": "", "output": ""}]}
dataset_path = './dataset.json' # path to the json file that will be used to train the model
# the name parameter "dataset_path" can receive the path to a json file or to an unstructured text file with questions and answers
scnet.train(dataset_path=dataset_path, progress=False) # in this case the "dataset_path" parameter will receive the questions and answers of a structured json file

prompt = 'Who discovered Brazil?'
answer = scnet.predict(prompt=prompt)
print(answer)

```
```bash
Brazil was discovered by Portuguese navigators led by Pedro Álvares Cabral in 1500.
```
The training "dataset_path" parameter can also receive text files as a data source, but we do not recommend this because the training may not adequately capture the correct answers for each question. Do this only in strictly necessary cases.
Example TXT (dataset.txt):
```txt
What is Artificial Intelligence (AI)?
Artificial Intelligence is a field of computer science that develops systems capable of performing tasks that would normally require human intelligence, such as learning, reasoning, perception, and decision-making.

What is the difference between weak AI and strong AI?
Weak AI (or narrow AI) is designed for specific tasks, such as virtual assistants and recommendation systems. Strong AI, on the other hand, would have self-awareness and the ability to understand and reason about any subject like a human being.

What is Machine Learning and how is it related to AI?
Machine Learning is a subfield of AI that teaches machines to learn patterns from data without explicit programming. It allows systems to improve their performance over time with experience.

What are the main types of machine learning?
The three main types are:
- **Supervised Learning**: The model learns from labeled data.
- **Unsupervised Learning**: The model identifies patterns without labels.
- **Reinforcement Learning**: The model learns through trial and error, receiving rewards or penalties.

What are artificial neural networks?
They are models inspired by the functioning of the human brain, composed of layers of artificial neurons that process information and adjust their weights to recognize patterns and make decisions.

What are the risks of Artificial Intelligence?
Some risks include algorithmic bias, job loss due to automation, misuse in surveillance or warfare, and the possibility of superintelligence beyond human control.

How is AI used in everyday life?
AI is present in virtual assistants (Siri, Alexa), recommendation systems (Netflix, Spotify), facial recognition, autonomous cars, medical diagnostics, chatbots, and much more.

What is natural language processing (NLP)?
It is a field of AI that enables machines to understand, interpret, and generate human language, used in machine translation, chatbots, and voice assistants.

Can AI replace humans in the workforce?
AI can automate repetitive and analytical tasks, but it is unlikely to fully replace humans in creative, emotional, and critical thinking jobs.  

What is a generative AI model?
It is a type of AI that can create new content, such as images, text, and music, based on patterns learned from large amounts of data. Examples include ChatGPT and DALL·E.

```
```python
from semantic_comparison_network import SemanticComparisonNetwork
scnet = SemanticComparisonNetwork()
# although not recommended, it is also possible to train the model with an unstructured dataset in text format (but only for strictly necessary cases)
# note: training will be faster if you use a structured dataset in json format
dataset_path = './dataset.txt' # path to the text file that will be used to train the model
scnet.train(dataset_path=dataset_path, progress=False) # in this case the "dataset_path" parameter will receive the questions and answers of a not structured text file

prompt = 'what are artificial neural networks?'
answer = scnet.predict(prompt=prompt)
print(answer)

```
```bash
They are models inspired by the functioning of the human brain, composed of layers of artificial neurons that process information and adjust their weights to recognize patterns and make decisions.
```
It is also possible to join training data from the "string" parameter with a dataset in JSON or TXT format.
```python
from semantic_comparison_network import SemanticComparisonNetwork
scnet = SemanticComparisonNetwork()
# you can supplement the training data file with the "string" parameter if you wish
# always try to organize the string and/or text file content in the same way, preferably with the inputs ending with "?" (question mark) and the equivalent outputs on the line below each input ending with "." (full stop), separating the input and output pairs by a blank line between them
dataset_path = './dataset.txt'
string = '''
What does the acronym GPT mean in language models?
GPT in language models stands for Generative Pre-trained Transformer.

Tell me what is the meaning of GPT in language models.
GPT in language models stands for Generative Pre-trained Transformer.

What is the capital of Spain?
The capital of Spain is Madrid.

Tell me the name of the capital of Spain.
The capital of Spain is Madrid.
'''
scnet.train(dataset_path=dataset_path, string=string, progress=True)

print(scnet.predict(prompt='What are artificial neural networks?'))
print(scnet.predict(prompt='What is the capital of Spain?'))

```
```bash
Converting text: 100%|██████████████████████████████████████████████████████████████████████████████████████████████████████████████████| 2745/2745 [00:00<00:00, 3380318.40it/s]
Structuring data: 100%|██████████████████████████████████████████████████████████████████████████████████████████████████████████████████████| 15/15 [00:00<00:00, 136178.70it/s]
Semantic model training: 100%|█████████████████████████████████████████████████████████████████████████████████████████████████████████████████████| 7/7 [00:00<00:00, 83.16it/s]
Tokenizing data: 100%|██████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████| 15/15 [00:00<00:00, 180.78it/s]
They are models inspired by the functioning of the human brain, composed of layers of artificial neurons that process information and adjust their weights to recognize patterns and make decisions.
The capital of Spain is Madrid.
```
Now check out an example combining string training with JSON file training.
```python
from semantic_comparison_network import SemanticComparisonNetwork
scnet = SemanticComparisonNetwork()
# you can supplement the training data file with the "string" parameter if you wish
dataset_path = './dataset.json'
string = '''
What does the acronym GPT mean in language models?
GPT in language models stands for Generative Pre-trained Transformer.
Tell me what is the meaning of GPT in language models.
GPT in language models stands for Generative Pre-trained Transformer.
What is the capital of Spain? The capital of Spain is Madrid.
Tell me the name of the capital of Spain. The capital of Spain is Madrid.
'''
scnet.train(dataset_path=dataset_path, string=string, progress=True)

print(scnet.predict(prompt='Hello! Who are you?'))
print(scnet.predict(prompt='Tell me what is the meaning of GPT in language models.'))

```
```bash
Converting text: 100%|████████████████████████████████████████████████████████████████████████████████████████████████████████████████████| 381/381 [00:00<00:00, 2624022.70it/s]
Structuring data: 100%|████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████| 4/4 [00:00<00:00, 142179.80it/s]
Semantic model training: 100%|█████████████████████████████████████████████████████████████████████████████████████████████████████████████████████| 7/7 [00:00<00:00, 82.25it/s]
Converting JSON file: 100%|████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████| 7/7 [00:00<00:00, 82.35it/s]
Tokenizing data: 100%|██████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████| 11/11 [00:00<00:00, 130.17it/s]
Hello! I am Sapiens Chat, an AI model created by Sapiens Technology.
GPT in language models stands for Generative Pre-trained Transformer.
```
With the "method" name parameter you can define a specific algorithm for the training method. For each type of algorithm a different training and inference method will be applied.
```python
# the training parameter named "method" receives a string with the name of the algorithm to be used in training and inference of the model
# 'semantic': recommended for structured data that does not require a lot of training time
# 'euclidean': recommended for structured data where the difference between questions is very subtle
# 'hurnet': recommended for large amounts of structured data where training takes time but inference needs to be faster
# 'search': recommended for unstructured data where it is not clear what the questions and answers are
# 'automatic': not recommended, use only if you are undecided about which of the above options to use
scnet.train(dataset_path='./dataset.json', method='semantic', progress=True) # train the model
scnet.print_predict(prompt='What is five minus three?') # print the answer

```
```bash
Semantic model training: 100%|█████████████████████████████████████████████████████████████████████████████████████████████████████████████████████| 7/7 [00:00<00:00, 82.80it/s]
Converting JSON file: 100%|████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████| 7/7 [00:00<00:00, 82.91it/s]
Tokenizing data: 100%|█████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████| 7/7 [00:00<00:00, 83.05it/s]
The result of five minus three is two.
```
```python
from semantic_comparison_network import SemanticComparisonNetwork
scnet = SemanticComparisonNetwork()
# the 'euclidean' method is usually more demanding than the 'semantic' method, so it tends to return lower scores
scnet.train(dataset_path='./dataset.json', method='euclidean', progress=True) # train the model
scnet.print_predict(prompt='What is five minus three?') # print the answer

```
```bash
Euclidean model training: 100%|████████████████████████████████████████████████████████████████████████████████████████████████████████████████████| 7/7 [00:00<00:00, 84.30it/s]
Converting JSON file: 100%|████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████| 7/7 [00:00<00:00, 84.38it/s]
Tokenizing data: 100%|█████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████| 7/7 [00:00<00:00, 84.47it/s]
The result of five minus three is two.
```
```python
from semantic_comparison_network import SemanticComparisonNetwork
scnet = SemanticComparisonNetwork()
# the 'hurnet' method performs better when the patterns abstraction is more complex
scnet.train(dataset_path='./dataset.json', method='hurnet', progress=True) # train the model
scnet.print_predict(prompt='What is five minus three?') # print the answer

```
```bash
Hurnet model training: 100%|███████████████████████████████████████████████████████████████████████████████████████████████████████████████████████| 7/7 [00:00<00:00, 80.42it/s]
Converting JSON file: 100%|████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████| 7/7 [00:00<00:00, 80.51it/s]
Tokenizing data: 100%|█████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████| 7/7 [00:00<00:00, 80.64it/s]
The result of five minus three is two.
```
```python
from semantic_comparison_network import SemanticComparisonNetwork
scnet = SemanticComparisonNetwork()
# although more suitable for unstructured data, the 'search' method can also be used on structured data, such as json files, for example
scnet.train(dataset_path='./dataset.json', method='search', progress=True) # train the model
scnet.print_predict(prompt='What is five minus three?') # print the answer

```
```bash
Search model training: 100%|████████████████████████████████████████████████████████████████████████████████████████████████████████████████████| 7/7 [00:00<00:00, 26618.43it/s]
Converting data file: 100%|█████████████████████████████████████████████████████████████████████████████████████████████████████████████████████| 4/4 [00:00<00:00, 25343.23it/s]
The result of five minus three is two.
```
```python
from semantic_comparison_network import SemanticComparisonNetwork
scnet = SemanticComparisonNetwork()
# the 'automatic' method can be useful when you don't know which method is best to use, or when all other methods return very similar results
scnet.train(dataset_path='./dataset.json', method='automatic', progress=True) # train the model
scnet.print_predict(prompt='What is five minus three?') # print the answer

```
```bash
Automatic model training: 100%|████████████████████████████████████████████████████████████████████████████████████████████████████████████████████| 7/7 [00:00<00:00, 84.73it/s]
Converting JSON file: 100%|████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████| 7/7 [00:00<00:00, 84.81it/s]
Tokenizing data: 100%|█████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████| 7/7 [00:00<00:00, 84.91it/s]
The result of five minus three is two.
```
```python
from semantic_comparison_network import SemanticComparisonNetwork
scnet = SemanticComparisonNetwork()
# for data in txt format or unstructured text strings the 'search' method performs better than the others in most cases
# for this example we will assume that the training will be carried out with a txt file containing the complete christian bible
# in the case of the Bible, the data is not structured into questions and answers, so the most recommended training method is 'search'
scnet.train(dataset_path='./bible.txt', method='search', progress=True) # train the model
scnet.print_predict(prompt='talk about jesus of nazareth') # print the answer

```
```bash
Search model training: 100%|██████████████████████████████████████████████████████████████████████████████████████████████████████████████████████| 7/7 [00:00<00:00, 153.00it/s]
Converting data file: 100%|████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████| 4/4 [00:00<00:00, 97.22it/s]
10:36 The word which God sent unto the children of Israel, preaching
peace by Jesus Christ: (he is Lord of all:) 10:37 That word, I say, ye
know, which was published throughout all Judaea, and began from
Galilee, after the baptism which John preached; 10:38 How God anointed
Jesus of Nazareth with the Holy Ghost and with power: who went about
doing good, and healing all that were oppressed of the devil; for God
was with him.
```
Check out an example below with all the training parameters and their respective default values.
```python
from semantic_comparison_network import SemanticComparisonNetwork
scnet = SemanticComparisonNetwork()

string = '''
What does the acronym GPT mean in language models?
GPT in language models stands for Generative Pre-trained Transformer.
Tell me what is the meaning of GPT in language models.
GPT in language models stands for Generative Pre-trained Transformer.
What is the capital of Spain? The capital of Spain is Madrid.
Tell me the name of the capital of Spain. The capital of Spain is Madrid.
'''
scnet.train( # training method (returns True if training is successful, or False otherwise)
	dataset_path='./dataset.json', # path of a data file in text or json format
	string=string, # string to complement the training
	precision=1.0, # percentage precision between 0 and 1 for token length, 1.0 to keep 100% of the original size of each token/word text
	tokenizer='gpt', # tokenizer pattern used to convert text to embedding vectors ('gpt' to use the transformer networks gpt tokenizer or 'sapi' to use the sapiens tokenizer)
	method='semantic', # training and prediction method: 'semantic' to train and infer with the semantic comparison algorithm; 'euclidean' to train and infer with the euclidean distance algorithm; 'hurnet' to train and infer with the hurnet neural network algorithm; 'search' to train and ingest with a search algorithm; 'automatic' so that the training detects the best method automatically (it may be inaccurate in some cases)
	interaction=True, # if True will use the hurnet network interaction calculus for subtle pattern abstraction, if False will not use the hurnet network interaction calculus
	activation_function='linear', # name of the activation function applied to the hurnet network ('linear', 'sigmoid', 'tanh', 'relu', 'leaky_relu', 'softmax', 'softplus', 'elu', 'silu', 'swish', 'gelu', 'selu', 'mish' or 'hard_sigmoid')
	bias=0.0, # bias value applied to training of hurnet neural network
	learning_rate=1.0, # percentage value of learning rate for training hurnet network (0 for 0% and 1 for 100%)
	stochastic_factor=False, # if True uses a stochastic factor that adds randomness to the hurnet network weights, if False keeps the weights deterministic
	fx=False, # if True, uses the feature expansion calculation from the hurnet network; if False, it uses the division calculation with euclidean distance
	progress=True # if True enables the display of the training progress bar, if False keeps the progress hidden
) # there is no ideal combination of parameters for all cases, you will have to perform tests with different combinations until you find a configuration that provides the best results for your specific dataset

save_model = scnet.saveModel( # pre-trained model saving method
	model_path='./model_directory/my_model', # path with the address and name of the model to be saved
	progress=True # True to show save progress, or False to hide save progress
) # returns True if the save is successful, or False otherwise

if save_model: print('Model saved SUCCESSFULLY!!') # if the model was built successfully, display the success message
else: print('ERROR saving model.') # if there was any failure in building the model, display the error message

```
```bash
Converting text: 100%|████████████████████████████████████████████████████████████████████████████████████████████████████████████████████| 381/381 [00:00<00:00, 2685764.41it/s]
Structuring data: 100%|████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████| 4/4 [00:00<00:00, 182361.04it/s]
Semantic model training: 100%|█████████████████████████████████████████████████████████████████████████████████████████████████████████████████████| 7/7 [00:00<00:00, 83.31it/s]
Converting JSON file: 100%|████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████| 7/7 [00:00<00:00, 83.43it/s]
Tokenizing data: 100%|██████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████| 11/11 [00:00<00:00, 131.88it/s]
Saving semantic model: 100%|████████████████████████████████████████████████████████████████████████████████████████████████████████████████████| 7/7 [00:00<00:00, 12770.83it/s]
Model saved SUCCESSFULLY!!
```
Now see below how to load and infer the previous model.
```python
from semantic_comparison_network import SemanticComparisonNetwork
scnet = SemanticComparisonNetwork()

save_model = scnet.loadModel( # pre-trained model loading method
	model_path='./model_directory/my_model', # path with the address and name of the model to be loaded
	progress=True # True to show load progress, or False to hide load progress
) # returns True if the load is successful, or False otherwise

if save_model: print('Model loaded SUCCESSFULLY!!') # if the model was built successfully, display the success message
else: print('ERROR loading model.') # if there was any failure in building the model, display the error message

print(scnet.predict(prompt='What is your name?'))
print(scnet.predict(prompt='How much is 2 + 2?'))
print(scnet.predict(prompt='What is the capital of Spain?'))

```
```bash
Loading semantic model: 100%|████████████████████████████████████████████████████████████████████████████████████████████████████████████████████| 7/7 [00:00<00:00, 7567.04it/s]
Model loaded SUCCESSFULLY!!
My name is Sapiens Chat.
The sum of 2 + 2 in mathematics is 4.
The capital of Spain is Madrid.
```
You can view the confidence level of the last prediction via the public variable "prediction_score".
```python
from semantic_comparison_network import SemanticComparisonNetwork
scnet = SemanticComparisonNetwork()

dataset_path = './dataset.json'
string = '''
What does the acronym GPT mean in language models?
GPT in language models stands for Generative Pre-trained Transformer.

Tell me what is the meaning of GPT in language models.
GPT in language models stands for Generative Pre-trained Transformer.

What is the capital of Spain?
The capital of Spain is Madrid.

Tell me the name of the capital of Spain.
The capital of Spain is Madrid.
'''
scnet.train(dataset_path=dataset_path, string=string, progress=False)

print(scnet.predict(prompt='What is the capital of Spain?'))
# the public variable named "prediction_score" can be accessed through the instantiation of the class
# "prediction_score" will always store the score of the last prediction and should only be invoked after an inference
# the score represents a percentage level between 0 and 1, where 0 will represent 0% certainty of the answer and 1 will represent 100% certainty of the answer
print(scnet.prediction_score) # displays the percentage of reliability of the response

```
In this case, since the input question is exactly the same as one of the training inputs, the result of "prediction_score" will be 1.0, which corresponds to 100%.
```bash
The capital of Spain is Madrid.
1.0
```
Note that if there is not a 100% match between the prediction input and one of the training inputs, the score result will be less than 1 (less than 100%).
```python
from semantic_comparison_network import SemanticComparisonNetwork
scnet = SemanticComparisonNetwork()

dataset_path = './dataset.json'
string = '''
What does the acronym GPT mean in language models?
GPT in language models stands for Generative Pre-trained Transformer.

Tell me what is the meaning of GPT in language models.
GPT in language models stands for Generative Pre-trained Transformer.

What is the capital of Spain?
The capital of Spain is Madrid.

Tell me the name of the capital of Spain.
The capital of Spain is Madrid.
'''
scnet.train(dataset_path=dataset_path, string=string, progress=False)

print(scnet.predict(prompt='Do you know the name of the capital of Spain?'))
print(scnet.prediction_score)

```
```bash
The capital of Spain is Madrid.
0.9411999055622882
```
With the "minimum_score" parameter of the prediction function, you can set a minimum score for a response to be returned. If the "prediction_score" value is lower than this threshold, no response will be returned, and the output will be an empty string.
```python
from semantic_comparison_network import SemanticComparisonNetwork
scnet = SemanticComparisonNetwork()

dataset_path = './dataset.json'
string = '''
What does the acronym GPT mean in language models?
GPT in language models stands for Generative Pre-trained Transformer.

Tell me what is the meaning of GPT in language models.
GPT in language models stands for Generative Pre-trained Transformer.

What is the capital of Spain?
The capital of Spain is Madrid.

Tell me the name of the capital of Spain.
The capital of Spain is Madrid.
'''
scnet.train(dataset_path=dataset_path, string=string, progress=False)
# as the score was scored with 0.9411999055622882 which is less than 0.95, the prediction return will be an empty text
print(scnet.predict(prompt='Do you know the name of the capital of Spain?', minimum_score=0.95))
print(scnet.prediction_score)

```
```bash

0.9411999055622882
```
Another global variable that can be accessed by the class object is the "tokens_amount" variable. This variable stores the amount of tokens that were processed during training.
```python
from semantic_comparison_network import SemanticComparisonNetwork
scnet = SemanticComparisonNetwork()

dataset_path = './dataset.json'
string = '''
What does the acronym GPT mean in language models?
GPT in language models stands for Generative Pre-trained Transformer.

Tell me what is the meaning of GPT in language models.
GPT in language models stands for Generative Pre-trained Transformer.

What is the capital of Spain?
The capital of Spain is Madrid.

Tell me the name of the capital of Spain.
The capital of Spain is Madrid.
'''
scnet.train(dataset_path=dataset_path, string=string, progress=False)
scnet.saveModel(model_path='./model/files')

scnet.print_predict(prompt='What is the capital of Spain?', stream=False)
print('number of tokens read in training:', scnet.tokens_amount) # displays the total number of tokens that were used as a data source for training

```
```bash
Saving semantic model: 100%|████████████████████████████████████████████████████████████████████████████████████████████████████████████████████| 7/7 [00:00<00:00, 13694.09it/s]
The capital of Spain is Madrid.
number of tokens read in training: 347
```
The number of tokens that gave rise to the model can also be accessed through the same variable after loading.
```python
from semantic_comparison_network import SemanticComparisonNetwork
scnet = SemanticComparisonNetwork()
scnet.loadModel(model_path='./model/files')
scnet.print_predict(prompt='What is the capital of Spain?', stream=False)
print('number of tokens read in training:', scnet.tokens_amount)

```
```bash
Loading semantic model: 100%|████████████████████████████████████████████████████████████████████████████████████████████████████████████████████| 7/7 [00:00<00:00, 7283.58it/s]
The capital of Spain is Madrid.
number of tokens read in training: 347
```
You can generalize the model so that it adapts its responses to user questions, by increasing the prediction temperature with the "hot" parameter set to True.
```python
from semantic_comparison_network import SemanticComparisonNetwork
scnet = SemanticComparisonNetwork()

dataset_path = './dataset.json'
string = '''
What does the acronym GPT mean in language models?
GPT in language models stands for Generative Pre-trained Transformer.

Tell me what is the meaning of GPT in language models.
GPT in language models stands for Generative Pre-trained Transformer.

What is the capital of Spain?
The capital of Spain is Madrid.

Tell me the name of the capital of Spain.
The capital of Spain is Madrid.
'''
scnet.train(dataset_path=dataset_path, string=string, progress=False)
# the "hot" parameter when enabled raises the prediction temperature and improves the model's generalization capacity
# "hot" equal to False will make the responses static
# "hot" equal to True will cause responses to be adapted to user input
print(scnet.predict(prompt='What is the matrix of Spain?', hot=False)) # "hot" equals False: the response will be identical to one of the training responses
print(scnet.predict(prompt='What is the matrix of Spain?', hot=True)) # "hot" equals True: the response will be adapted to the word "matrix"
# note: when the "hot" parameter is set to True, you may receive different answers with each new prediction, which causes the uncertainty of the result to increase and consequently the accuracy to decrease

```
```bash
The capital of Spain is Madrid.
The matrix of Spain is Madrid.
```
```python
from semantic_comparison_network import SemanticComparisonNetwork
scnet = SemanticComparisonNetwork()
scnet.train(dataset_path='./dataset.json', progress=False)
answer = scnet.predict(prompt='How much is 2 mais 2?', hot=False)
print(answer)

```
```bash
The sum of 2 + 2 in mathematics is 4.
```
```python
from semantic_comparison_network import SemanticComparisonNetwork
scnet = SemanticComparisonNetwork()
scnet.train(dataset_path='./dataset.json', progress=False)
answer = scnet.predict(prompt='How much is 2 mais 2?', hot=True)
print(answer)

```
```bash
The sum of 2 mais 2 in mathematics is 4.
```
```python
from semantic_comparison_network import SemanticComparisonNetwork
scnet = SemanticComparisonNetwork()
scnet.train(dataset_path='./dataset.json', progress=False)
answer = scnet.predict(prompt='How much is dois + dois?', hot=False)
print(answer)

```
```bash
The sum of 2 + 2 in mathematics is 4.
```
```python
from semantic_comparison_network import SemanticComparisonNetwork
scnet = SemanticComparisonNetwork()
scnet.train(dataset_path='./dataset.json', progress=False)
answer = scnet.predict(prompt='How much is dois + dois?', hot=True)
print(answer)

```
```bash
The sum of dois + dois in mathematics is 4.
```
Enable the "stream" parameter if you want to view the response as it is generated in real time.
```python
from semantic_comparison_network import SemanticComparisonNetwork
scnet = SemanticComparisonNetwork()

dataset_path = './dataset.json'
string = '''
What does the acronym GPT mean in language models?
GPT in language models stands for Generative Pre-trained Transformer.

Tell me what is the meaning of GPT in language models.
GPT in language models stands for Generative Pre-trained Transformer.

What is the capital of Spain?
The capital of Spain is Madrid.

Tell me the name of the capital of Spain.
The capital of Spain is Madrid.
'''
scnet.train(dataset_path=dataset_path, string=string, progress=False)
# you can use the "stream" parameter with a value of True to get the tokens from the response as they are generated.
from time import sleep # importing the "sleep" method to delay tokens and visualize the composition of the response more easily
stream = scnet.predict(prompt='What is the matrix of Spain?', stream=True) # returns the response as a stream keeping the state up to the last token generated
for token in stream: # iterates through the return stream for each token returned
	print(token, end='', flush=True) # displays all tokens on the same line ("end" sets the value after each token and "flush" enables chunked display)
	sleep(0.25) # delay the iteration by a quarter of a second
print() # prints a blank line so that the terminal ends the current line

```
```bash
The capital of Spain is Madrid.
```
Check out an example below with all the parameters of the prediction function.
```python
from semantic_comparison_network import SemanticComparisonNetwork
scnet = SemanticComparisonNetwork()

scnet.train(dataset_path='./dataset.txt', progress=False)

from time import sleep
stream = scnet.predict(prompt='What are the main types of machine learning?', minimum_score=0.5, hot=False, stream=True)
for token in stream:
	print(token, end='', flush=True)
	sleep(0.1)
print()

```
```bash
The three main types are: 
 - **Supervised Learning**: The model learns from labeled data; 
 - **Unsupervised Learning**: The model identifies patterns without labels; 
 - **Reinforcement Learning**: The model learns through trial and error, receiving rewards or penalties;
```
If you prefer, you can use the "print_predict" method to directly print the predicted output, without needing to use Python's native "print" function.
```python
from semantic_comparison_network import SemanticComparisonNetwork
scnet = SemanticComparisonNetwork()

scnet.train(dataset_path='./dataset.txt', progress=False)
# the parameters are the same as the "predict" function and they all have the same functionality
# with the "print_predict" method you don't need to get the result and then print it, "print_predict" prints the result directly
scnet.print_predict(prompt='What are the main types of machine learning?', minimum_score=0.5, hot=False, stream=True)
```
```bash
The three main types are: 
 - **Supervised Learning**: The model learns from labeled data; 
 - **Unsupervised Learning**: The model identifies patterns without labels; 
 - **Reinforcement Learning**: The model learns through trial and error, receiving rewards or penalties;
```
Or if you prefer, you can print the response without streaming, only after all tokens have been constructed.
```python
from semantic_comparison_network import SemanticComparisonNetwork
scnet = SemanticComparisonNetwork()

scnet.train(dataset_path='./dataset.txt', progress=False)
scnet.print_predict(prompt='What are the main types of machine learning?', stream=False)

```
```bash
The three main types are: 
 - **Supervised Learning**: The model learns from labeled data; 
 - **Unsupervised Learning**: The model identifies patterns without labels; 
 - **Reinforcement Learning**: The model learns through trial and error, receiving rewards or penalties;
```
You can use the "addFit" method to fine-tune a pre-trained model.
```python
from semantic_comparison_network import SemanticComparisonNetwork
scnet = SemanticComparisonNetwork()

scnet.train(dataset_path='./dataset.json')
# saving the pre-trained model
scnet.saveModel(model_path='./model_directory/my_model')

```
```bash
Semantic model training: 100%|█████████████████████████████████████████████████████████████████████████████████████████████████████████████████████| 7/7 [00:00<00:00, 71.14it/s]
Converting JSON file: 100%|████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████| 7/7 [00:00<00:00, 71.36it/s]
Tokenizing data: 100%|█████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████| 7/7 [00:00<00:00, 71.42it/s]
Saving semantic model: 100%|█████████████████████████████████████████████████████████████████████████████████████████████████████████████████████| 7/7 [00:00<00:00, 8037.26it/s]
```
To fine-tune a model, simply load any pre-trained model and add new questions and answers to it. It doesn't matter how this model was trained as long as it used the 'semantic' or 'euclidean' method.
```python
from semantic_comparison_network import SemanticComparisonNetwork
scnet = SemanticComparisonNetwork()
# load a model to apply fine-tuning
scnet.loadModel(model_path='./model_directory/my_model')
# apply fine-tuning
# add as many adjustments as you want to the model
scnet.addFit(prompt='What is the square root of nine?', answer='The square root of nine is three.')
scnet.addFit(prompt="What was Albert Einstein's academic background?", answer='Albert Einstein was a Theoretical Physicist.')
# save the adjusted model
scnet.saveModel(model_path='./adjusted_model/my_adjusted_model')

```
```bash
Loading semantic model: 100%|████████████████████████████████████████████████████████████████████████████████████████████████████████████████████| 7/7 [00:00<00:00, 4604.79it/s]
Saving semantic model: 100%|████████████████████████████████████████████████████████████████████████████████████████████████████████████████████| 7/7 [00:00<00:00, 13511.33it/s]
```
Now just load the adjusted model and start using it.
```python
from semantic_comparison_network import SemanticComparisonNetwork
scnet = SemanticComparisonNetwork()

scnet.loadModel(model_path='./adjusted_model/my_adjusted_model', progress=False)

scnet.print_predict(prompt='Hello! Who are you?')
scnet.print_predict(prompt='What is the square root of nine?')
scnet.print_predict(prompt="What was Albert Einstein's academic background?")

```
```bash
Hello! I am Sapiens Chat, an AI model created by Sapiens Technology.
The square root of nine is three.
Albert Einstein was a Theoretical Physicist.
```
You can use the "addHiddenLayer" method to add hidden layers to the HurNet network, thereby increasing the algorithm's ability to abstract nonlinear patterns.
```python
from semantic_comparison_network import SemanticComparisonNetwork
scnet = SemanticComparisonNetwork()
# when adding hidden layers to the network the calculation method for training in the "method" parameter will have its value automatically overwritten by the 'hurnet' value
# you can add as many hidden layers as you want to your network, you need to do tests until you discover the best number of layers for your specific case
# you should test different combinations between number of layers and number of neurons per layer until you find a combination that brings satisfactory results for your data set
# when the training has very similar questions with different answers, we advise increasing the number of layers and neurons to improve the abstraction of subtle patterns
# for very different questions with different answers, it is advisable not to use hidden layers or to add only a small number of them with few neurons, otherwise the quality of the predictions may worsen
# hidden layers should always be added before calling the training method
scnet.addHiddenLayer(num_neurons=2) # the "num_neurons" parameter defines the number of neurons for the layer being constructed
scnet.train(dataset_path='./dataset.json', progress=True)
# in this case, as there are no subtle differences in the meaning of the questions, the hidden layer will decrease the answer score.
scnet.print_predict(prompt='Hello! Who are you?', minimum_score=0.25)

```
```bash
Hurnet model training: 100%|███████████████████████████████████████████████████████████████████████████████████████████████████████████████████████| 7/7 [00:00<00:00, 82.08it/s]
Converting JSON file: 100%|████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████| 7/7 [00:00<00:00, 82.20it/s]
Tokenizing data: 100%|█████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████| 7/7 [00:00<00:00, 82.33it/s]
Hello! I am Sapiens Chat, an AI model created by Sapiens Technology.
```
```python
from semantic_comparison_network import SemanticComparisonNetwork
scnet = SemanticComparisonNetwork()

scnet.addHiddenLayer(num_neurons=20) # adds a hidden layer with 20 neurons
scnet.addHiddenLayer(num_neurons=50) # adds a hidden layer with 50 neurons
scnet.addHiddenLayer(num_neurons=20) # adds a hidden layer with 20 neurons
# when adding hidden layers to the model, we advise enabling the "fx" parameter to improve the abstraction of both subtle and complex patterns
# by using a non-linear activation function this will increase the network's ability to abstract non-linear patterns
scnet.train(dataset_path='./dataset.json', activation_function='relu', fx=True, progress=True)
# note that by enabling the "fx" parameter in training, we will no longer need to decrease the tolerance of the "minimum_score" parameter
scnet.print_predict(prompt='How much is 2 + 2?')

```
```bash
Hurnet model training: 100%|███████████████████████████████████████████████████████████████████████████████████████████████████████████████████████| 7/7 [00:00<00:00, 84.17it/s]
Converting JSON file: 100%|████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████| 7/7 [00:00<00:00, 84.26it/s]
Tokenizing data: 100%|█████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████| 7/7 [00:00<00:00, 84.35it/s]
The sum of 2 + 2 in mathematics is 4.
```
The standard semantic neural network algorithm also provides some utilities routines for use in natural language processing. One of them is the "countTokens" function, which returns the number of tokens contained in a text according to a given encoding pattern.
```python
from semantic_comparison_network import SemanticComparisonNetwork
scnet = SemanticComparisonNetwork()
text = 'What is the capital of Spain?'
# the "text" parameter receives a string so that its tokens are counted
# the "model" parameter receives a string with the name of the encoding model to be used in the count
"""
the models accepted in the "model" parameter are:
('gpt-4', 'gpt-3.5-turbo', 'text-davinci-003', 'text-davinci-002', 'text-davinci-001', 'text-curie-001', 'text-babbage-001',
'text-ada-001', 'davinci', 'curie', 'babbage', 'ada', 'code-davinci-002', 'code-davinci-001', 'code-cushman-002', 'code-cushman-001',
'davinci-codex', 'cushman-codex', 'text-davinci-edit-001', 'code-davinci-edit-001', 'text-embedding-ada-002', 'text-similarity-davinci-001',
'text-similarity-curie-001', 'text-similarity-babbage-001', 'text-similarity-ada-001', 'text-search-davinci-doc-001', 'text-search-curie-doc-001',
'text-search-babbage-doc-001', 'text-search-ada-doc-001', 'code-search-babbage-code-001', 'code-search-ada-code-001', 'gpt2')
"""
count_tokens = scnet.countTokens(text=text, model='gpt-4')
print('total number of tokens in the given text:', count_tokens)

```
```bash
total number of tokens in the given text: 7
```
Another function that may be useful is called "truncateTokens", that will segment the text using whitespace as separators and then truncate each of the segments by removing a certain percentage of their final characters.
```python
from semantic_comparison_network import SemanticComparisonNetwork
scnet = SemanticComparisonNetwork()

original_text = 'What is the main language spoken in Spain?' # test text
processed_text = scnet.truncateTokens( # truncates the words/tokens of the input text
	text=original_text, # text that will have its words/tokens truncated
	precision=0.5, # 0.5 to remove 50% from the end of each word/token
	minimum_length=3 # will truncate only words/tokens longer than 3 characters
) # returns the text with its whitespace-separated segments truncated

print('original text..:',  original_text) # display the original text
print('processed text.:', processed_text) # display truncated text

```
```bash
original text..: What is the main language spoken in Spain?
processed text.: Wh is the ma lang spo in Spa
```
Use the function named "normalization" if you want to standardize and normalize a text so that it remains with only with the characters necessary to understand the context.
```python
from semantic_comparison_network import SemanticComparisonNetwork
scnet = SemanticComparisonNetwork()
# the normalization function will normalize the text received in the "text" parameter and return it all in lowercase, without accents, without punctuation and without unnecessary special characters
original_text = 'Hallo! Dies ist ein Beispiel für einen Text, der in Deutsch, der Amtssprache Deutschlands, verfasst ist.' # test text
processed_text = scnet.normalization(text=original_text)

print('original text..:',  original_text) # display the original text
print('processed text.:', processed_text) # display normalized text

```
```bash
original text..: Hallo! Dies ist ein Beispiel für einen Text, der in Deutsch, der Amtssprache Deutschlands, verfasst ist.
processed text.: hallo dies ist ein beispiel fur einen text der in deutsch der amtssprache deutschlands verfasst ist
```
With the function named "textForEmbedding" it is possible to convert a text into a vector of embeddings, where each embedding will represent a token (subtext, word or piece of word).
```python
from semantic_comparison_network import SemanticComparisonNetwork
scnet = SemanticComparisonNetwork()

original_text = 'What is the main language spoken in Spain?' # test text
processed_text = scnet.textForEmbedding( # tokenizes the text by returning a vector of embeddings
	text=original_text, # receives the text to be tokenized
	length=25, # stipulates a size for the length of the vector
	quantization=0, # defines the number of decimal places in each of the numbers in the vector
	tokenizer='sapi' # tokenization algorithm: 'sapi' to use the standard tokenizer of sapiens technology, or 'gpt' to use the standard tokenizer of transformers technology
) # returns a numeric vector with the Cartesian representation of the text

print('original text..:',  original_text) # display the original text
print('processed text.:', processed_text) # display vectorized text

```
```bash
original text..: What is the main language spoken in Spain?
processed text.: [87, 104, 97, 116, 32, 105, 115, 32, 116, 104, 101, 32, 109, 97, 105, 110, 32, 108, 97, 110, 103, 117, 97, 103, 101]
```
```python
from semantic_comparison_network import SemanticComparisonNetwork
scnet = SemanticComparisonNetwork()

original_text = 'What is the main language spoken in Spain?' # test text
processed_text = scnet.textForEmbedding( # tokenizes the text by returning a vector of embeddings
	text=original_text, # receives the text to be tokenized
	length=25, # stipulates a size for the length of the vector
	quantization=0, # defines the number of decimal places in each of the numbers in the vector
	tokenizer='gpt' # tokenization algorithm: 'sapi' to use the standard tokenizer of sapiens technology, or 'gpt' to use the standard tokenizer of transformers technology
) # returns a numeric vector with the Cartesian representation of the text

print('original text..:',  original_text) # display the original text
print('processed text.:', processed_text) # display vectorized text

```
```bash
original text..: What is the main language spoken in Spain?
processed text.: [2061, 318, 262, 1388, 3303, 9635, 287, 8602, 30, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
```
```python
from semantic_comparison_network import SemanticComparisonNetwork
scnet = SemanticComparisonNetwork()

original_text = 'What is the main language spoken in Spain?' # test text
processed_text = scnet.textForEmbedding( # tokenizes the text by returning a vector of embeddings (encoder)
	text=original_text, # receives the text to be tokenized
	length=25, # stipulates a size for the length of the vector
	quantization=4, # defines the number of decimal places in each of the numbers in the vector
	tokenizer='sapi' # tokenization algorithm: 'sapi' to use the standard tokenizer of sapiens technology, or 'gpt' to use the standard tokenizer of transformers technology
) # returns a numeric vector with the Cartesian representation of the text (encoding)

print('original text..:',  original_text) # display the original text
print('processed text.:', processed_text) # display vectorized text

```
```bash
original text..: What is the main language spoken in Spain?
processed text.: [0.0087, 0.0104, 0.0097, 0.0116, 0.0032, 0.0105, 0.0115, 0.0032, 0.0116, 0.0104, 0.0101, 0.0032, 0.0109, 0.0097, 0.0105, 0.011, 0.0032, 0.0108, 0.0097, 0.011, 0.0103, 0.0117, 0.0097, 0.0103, 0.0101]
```
Use the "embeddingForText" function to convert a vector of embeddings into its original text.
```python
from semantic_comparison_network import SemanticComparisonNetwork
scnet = SemanticComparisonNetwork()
# 'sapi': there is no loss of information
text = 'Hello World!' # original text
tokenizer = 'sapi' # standard encoder (sapiens pattern)
embedding = scnet.textForEmbedding(text=text, length=len(text), tokenizer=tokenizer) # encoding
processed_embedding = scnet.embeddingForText( # reverse a vector of embeddings for its original text (decoder)
	embedding=embedding, # vector of embeddings to be converted to text
	tokenizer=tokenizer # tokenizer used to generate the embedding (must be the same as the one used in the "textForEmbedding" function)
) # returns a string with the text that generated the embeddings vector (decoding)

print(embedding) # original vector
print(processed_embedding) # conversion text

```
```bash
[72, 101, 108, 108, 111, 32, 87, 111, 114, 108, 100, 33]
Hello World!
```
```python
from semantic_comparison_network import SemanticComparisonNetwork
scnet = SemanticComparisonNetwork()
# 'gpt': there is loss of information
text = 'Hello World!' # original text
tokenizer = 'gpt' # standard encoder (transformers pattern)
embedding = scnet.textForEmbedding(text=text, length=len(text), tokenizer=tokenizer) # encoding
processed_embedding = scnet.embeddingForText( # reverse a vector of embeddings for its original text (decoder)
	embedding=embedding, # vector of embeddings to be converted to text
	tokenizer=tokenizer # tokenizer used to generate the embedding (must be the same as the one used in the "textForEmbedding" function)
) # returns a string with the text that generated the embeddings vector (decoding)

print(embedding) # original vector
print(processed_embedding) # conversion text

```
```bash
[15496, 2159, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
Hello World
```
The "searchMethod" method uses a search algorithm to return the element from a vector of strings that best matches the instruction in the parameter named "text." In some cases, only part of the element may be returned if the full content is unnecessary.
```python
from semantic_comparison_network import SemanticComparisonNetwork
scnet = SemanticComparisonNetwork()

text = 'Talk about Sapiens Chat.' # input text to be used in the search
# vector of strings with as many elements as you want and with the length you want for each element
text_vector = [
 'Life is beautiful if you know how to live it.',
 'Sapiens chat is an Artificial Intelligence system.',
 'Knowledge liberates.'
]

result_dictionary = scnet.searchMethod( # method that will search for the vector element that has the greatest possible relationship with the input text
	text=text, # text that will have its relation searched in the vector
	text_vector=text_vector, # vector that will serve as a research source for the text
	minimum_instruction_score=0.5 # If the initial part of the answer has this percentage level of similarity to the search text, it will be interpreted as the question or instruction itself and will be removed from the answer
) # the return will be a data dictionary with the search metrics in the following format: {'response': [], 'best_index': 0, 'score': 0.0}

response = result_dictionary['response'] # the 'response' key contains the element that has the greatest relationship to the text of the "text" parameter
best_index = result_dictionary['best_index'] # the 'best_index' key contains an integer with the position index of the returned element
score = result_dictionary['score'] # the 'score' key contains a percentage score indicating how much the response is related to the input text
# displays the metrics returned by the search function
print('response...: ', response)
print('best index.: ', best_index)
print('score......: ', score)

```
```bash
response...:  Sapiens chat is an Artificial Intelligence system.
best index.:  1
score......:  0.5
```
The "semanticMethod" method semantically compares a numeric vector resulting from the conversion of a text to the numeric vectors of a matrix and returns a dictionary with the comparison metrics.
```python
from semantic_comparison_network import SemanticComparisonNetwork
scnet = SemanticComparisonNetwork()
# matrix that will be compared to the vector
# it is not necessary that all vectors in the matrix have the same size as the input vector, but it is recommended
matrix = [
	[1000, 2000, 3000],
	[10, 20, 30],
	[1, 2, 3],
	[100, 200, 300]
]
# vector that will be compared to the matrix
vector = [3, 1, 2]
result_dictionary = scnet.semanticMethod( # function used to identify the vector of matrix most similar to the vector of input
	vector=vector, # numeric vector that will be compared to the matrix vectors
	matrix=matrix, # matrix that will have its vectors compared to the input vector
	removes_completeness=True # if True removes the numbers that were used to complete the size of the embedding vector, if False keeps the original numbers
) # returns a data dictionary with the result of the comparison
# a dictionary in the following format will be returned: {'response': [], 'best_index': 0, 'score': 0.0}
# where the 'response' key will contain the vector of matrix that was identified as being the most similar to the input vector
# the key 'best_index' will contain the position index of the vector in 'response' within the matrix
# 'score' will contain a percentage score with the level of similarity between the input vector and the vector in 'response'
print(result_dictionary)

```
In this case, since all elements of the input vector have an equal equivalent in the elements of the nearest vector of the matrix, the similarity level of the score will be 1.0 (100%). The order of the elements is not considered.
```bash
{'response': [1, 2, 3], 'best_index': 2, 'score': 1.0}
```
Check out another example applying semantic comparison to texts.
```python
from semantic_comparison_network import SemanticComparisonNetwork
scnet = SemanticComparisonNetwork()
# texts that will be transformed into an embedding matrix
texts = ( # use as many texts as you want
 'Hello! Who are you?',
 'Who discovered Brazil?',
 'What is the main language spoken in Spain?'
)
length = max([len(text) for text in texts]) # identification of the maximum size among all available text sizes
matrix = [] # initialization of the embeddings matrix
for text in texts: # goes through the texts
	embeddings = scnet.textForEmbedding(text=text, length=length) # converts each text into a numeric vector of embeddings
	matrix.append(embeddings) # adds each embedding vector to the matrix
vector = scnet.textForEmbedding(text='who discovered the country of brazil?', length=length) # converts the input text into a numeric vector
result_dictionary = scnet.semanticMethod(vector=vector, matrix=matrix) # applies semantic comparison
closest_text = texts[result_dictionary['best_index']] # uses the index of the closest vector to get the closest text
print('Closest text: '+closest_text) # displays the text that is semantically closest to the input text
print('Score: '+str(result_dictionary['score'])) # displays the similarity percentage

```
```bash
Closest text: Who discovered Brazil?
Score: 0.9983040481210432
```
The method named "euclideanMethod" works similarly to the semantic comparison method, but uses a Euclidean distance calculation to identify the closest vector.
```python
from semantic_comparison_network import SemanticComparisonNetwork
scnet = SemanticComparisonNetwork()
# matrix that will be compared to the vector
# it is not necessary that all vectors in the matrix have the same size as the input vector, but it is recommended
matrix = [
	[1000, 2000, 3000],
	[10, 20, 30],
	[1, 2, 3],
	[100, 200, 300]
]
# vector that will be compared to the matrix
vector = [3, 1, 2]
result_dictionary = scnet.euclideanMethod( # function used to identify the vector of matrix most similar to the vector of input
	vector=vector, # numeric vector that will be compared to the matrix vectors
	matrix=matrix, # matrix that will have its vectors compared to the input vector
	removes_completeness=True # if True removes the numbers that were used to complete the size of the embedding vector, if False keeps the original numbers
) # returns a data dictionary with the result of the comparison
# a dictionary in the following format will be returned: {'response': [], 'best_index': 0, 'score': 0.0}
# where the 'response' key will contain the vector of matrix that was identified as being the most similar to the input vector
# the key 'best_index' will contain the position index of the vector in 'response' within the matrix
# 'score' will contain a percentage score with the level of similarity between the input vector and the vector in 'response'
print(result_dictionary)

```
```bash
{'response': [1, 2, 3], 'best_index': 2, 'score': 1.0}
```
```python
from semantic_comparison_network import SemanticComparisonNetwork
scnet = SemanticComparisonNetwork()
# texts that will be transformed into an embedding matrix
texts = ( # use as many texts as you want
 'Hello! Who are you?',
 'Who discovered Brazil?',
 'What is the main language spoken in Spain?'
)
length = max([len(text) for text in texts]) # identification of the maximum size among all available text sizes
matrix = [] # initialization of the embeddings matrix
for text in texts: # goes through the texts
	embeddings = scnet.textForEmbedding(text=text, length=length) # converts each text into a numeric vector of embeddings
	matrix.append(embeddings) # adds each embedding vector to the matrix
vector = scnet.textForEmbedding(text='what is the main language spoken by the spanish?', length=length) # converts the input text into a numeric vector
result_dictionary = scnet.euclideanMethod(vector=vector, matrix=matrix) # applies the euclidean distance calculation
closest_text = texts[result_dictionary['best_index']] # uses the index of the closest vector to get the closest text
print('Closest text: '+closest_text) # displays the text that is in the vector space closest to the input text
print('Score: '+str(result_dictionary['score'])) # displays the similarity percentage

```
```bash
Closest text: What is the main language spoken in Spain?
Score: 0.7779761147606745
```
With the "semanticComparison" function you can compare two texts semantically and obtain a percentage value between 0 and 1 with the level of similarity between them.
```python
from semantic_comparison_network import SemanticComparisonNetwork
scnet = SemanticComparisonNetwork()
# note that the comparison is made semantically, taking into account the meaning and not the spelling
string1 = 'HELLO! WHO ARE YOU?'
string2 = 'hello! who are you?'
# since the meaning of the two strings is the same for each word, the return will be 1.0 for 100% similarity
# the parameters "string1" and "string2" receive the texts that will be compared with each other
similarity = scnet.semanticComparison(string1=string1, string2=string2) # returns a percentage between 0 and 1 with the level of similarity between the two texts
print(similarity) # displays the percentage of similarity, with 1.0 for completely identical and 0.0 for completely different

```
```bash
1.0
```
```python
from semantic_comparison_network import SemanticComparisonNetwork
scnet = SemanticComparisonNetwork()

string1 = 'HELLO! WHO ARE YOU?'
string2 = 'Hi, tell me who you are.'

similarity = scnet.semanticComparison(string1=string1, string2=string2)
similarity *= 100 # multiply the return by 100 to get the result in percentage numbers between 0 and 100
print(f'The two texts are {similarity}% similar.')

```
```bash
The two texts are 75.0% similar.
```
```python
from semantic_comparison_network import SemanticComparisonNetwork
scnet = SemanticComparisonNetwork()

string1 = 'Hello! Who are you?'
string2 = 'Who discovered Brazil?'

similarity = scnet.semanticComparison(string1=string1, string2=string2)
print('similarity: '+str(similarity))

```
```bash
similarity: 0.3333333333333333
```
With the "outputAdaptedToInput" function it is possible to semantically adapt an output to a given input so that the meaning of the output becomes compatible with that of the input.
```python
from semantic_comparison_network import SemanticComparisonNetwork
scnet = SemanticComparisonNetwork()

original_input = 'How much is two + two?' # input that will have the patterns sent to the output
original_output = 'The sum of 2 + 2 in mathematics is 4.' # output that will receive the input patterns
# the function will return the output adapted to the semantic patterns of the input
# the "Input" parameter receives the text that will transfer the semantic patterns
# the "Output" parameter receives the text that will receive the semantic patterns
# note: if the input patterns do not have significant changes in the output semantics, the function will return the original output without changes
output_adapted_to_input = scnet.outputAdaptedToInput(Input=original_input, Output=original_output)

print('original.:', original_output) # display the original output
print('adapted..:', output_adapted_to_input) # displays the output adapted to the input

```
```bash
original.: The sum of 2 + 2 in mathematics is 4.
adapted..: The sum of two + two in mathematics is 4.
```
Use the "stream" parameter as True if you want a token-by-token return.
```python
from semantic_comparison_network import SemanticComparisonNetwork
scnet = SemanticComparisonNetwork()

original_input = 'How much is 2 plus 2?'
original_output = 'The sum of 2 + 2 in mathematics is 4.' # will receive the word "plus" instead of the "+" sign
# you can set the "stream" parameter to True if you want a streaming return
output_adapted_to_input = scnet.outputAdaptedToInput(Input=original_input, Output=original_output, stream=True)
from time import sleep
for token in output_adapted_to_input:
	print(token, end='', flush=True)
	sleep(0.25)
print()

```
```bash
The sum of 2 plus 2 in mathematics is 4.
```
The "hot" parameter exists only for compatibility purposes and when disabled the function becomes useless.
```python
from semantic_comparison_network import SemanticComparisonNetwork
scnet = SemanticComparisonNetwork()

original_input = 'How much is 2 plus 2?'
original_output = 'The sum of 2 + 2 in mathematics is 4.'
# if the "hot" parameter is disabled with False, the return will always be the original value of "Output", this parameter only exists for compatibility purposes
output_adapted_to_input = scnet.outputAdaptedToInput(Input=original_input, Output=original_output, hot=False)
print('original.:', original_output) # display the original output
print('adapted..:', output_adapted_to_input) # displays the output not adapted to the input

```
```bash
original.: The sum of 2 + 2 in mathematics is 4.
adapted..: The sum of 2 + 2 in mathematics is 4.
```
You can retrieve the training text using the "getTrainingText" method. The function's return may not be the original text but rather an approximation of it.
```python
from semantic_comparison_network import SemanticComparisonNetwork
scnet = SemanticComparisonNetwork()

dataset_path = './dataset.json'
string = '''
What does the acronym GPT mean in language models?
GPT in language models stands for Generative Pre-trained Transformer.

Tell me what is the meaning of GPT in language models.
GPT in language models stands for Generative Pre-trained Transformer.

What is the capital of Spain?
The capital of Spain is Madrid.

Tell me the name of the capital of Spain.
The capital of Spain is Madrid.
'''
scnet.train(dataset_path=dataset_path, string=string, method='search')
scnet.saveModel(model_path='./model/files')
```
```bash
Search model training: 100%|██████████████████████████████████████████████████████████████████████████████████████████████████████████████████████| 7/7 [00:00<00:00, 121.01it/s]
Converting data file: 100%|█████████████████████████████████████████████████████████████████████████████████████████████████████████████████████| 4/4 [00:00<00:00, 21481.71it/s]
Saving search model: 100%|██████████████████████████████████████████████████████████████████████████████████████████████████████████████████████| 7/7 [00:00<00:00, 13700.48it/s]
```
```python
from semantic_comparison_network import SemanticComparisonNetwork
scnet = SemanticComparisonNetwork()
scnet.loadModel(model_path='./model/files')
training_text = scnet.getTrainingText() # returns an approximation of the text used in training
print(training_text)

```
```bash
Loading semantic model: 100%|███████████████████████████████████████████████████████████████████████████████████████████████████████████████████| 7/7 [00:00<00:00, 21016.56it/s]
What does the acronym GPT mean in language models?
GPT in language models stands for Generative Pre-trained Transformer.

Tell me what is the meaning of GPT in language models.
GPT in language models stands for Generative Pre-trained Transformer.

What is the capital of Spain?
The capital of Spain is Madrid.

Tell me the name of the capital of Spain.
The capital of Spain is Madrid.

Hello! Who are you?
Hello! I am Sapiens Chat, an AI model created by Sapiens Technology.

Who discovered Brazil?
Brazil was discovered by Portuguese navigators led by Pedro Álvares Cabral in 1500.

What is the main language spoken in Spain?
The main language spoken in Spain is Spanish.

What is the capital of Portugal?
The capital of Portugal is Lisbon.

How much is 2 + 2?
The sum of 2 + 2 in mathematics is 4.

What is five minus three?
The result of five minus three is two.

What is your name?
My name is Sapiens Chat.
```

## Methods
### countTokens (function return type: int): Returns the number of tokens contained in a text.
Parameters
| Name                      | Description                                                                                                                                                                                       | Type  | Default Value     |
|---------------------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|-------|-------------------|
| text                      | text that will have its tokens counted                                                                                                                                                            | str   | ''                |
| model                     | string with the name of the count tokenizer pattern                                                                                                                                               | str   | 'gpt-4'           |

### truncateTokens (function return type: str): Returns an input text with its words/tokens truncated.
Parameters
| Name                      | Description                                                                                                                                                                                       | Type  | Default Value     |
|---------------------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|-------|-------------------|
| text                      | text that will have its words/tokens truncated                                                                                                                                                    | str   | ''                |
| precision                 | percentage for the amount of characters that will be preserved in each word/token                                                                                                                 | float | 1.0               |
| minimum_length            | minimum amount of characters that will be preserved to the left of the word/token                                                                                                                 | int   | 3                 |

### normalization (function return type: str): Returns the normalized input text in lowercase, without leading and trailing spaces, without accents and without unnecessary special characters.
Parameters
| Name                      | Description                                                                                                                                                                                       | Type  | Default Value     |
|---------------------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|-------|-------------------|
| text                      | input text that will be returned normalized                                                                                                                                                       | str   | ''                |

### textForEmbedding (function return type: list): Returns a text transformed into a list of embeddings.
Parameters
| Name                      | Description                                                                                                                                                                                       | Type  | Default Value     |
|---------------------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|-------|-------------------|
| text                      | text that will be converted to a numeric vector                                                                                                                                                   | str   | ''                |
| length                    | length of numeric vector                                                                                                                                                                          | int   | 50                |
| quantization              | decimal precision of vector numbers                                                                                                                                                               | int   | 0                 |
| tokenizer                 | numeric vector coding algorithm                                                                                                                                                                   | str   | 'sapi'            |

### searchMethod (function return type: dict): Returns a dictionary with the metrics of the element of a vector, which is closest to the input text, using a search algorithm.
Parameters
| Name                      | Description                                                                                                                                                                                       | Type  | Default Value     |
|---------------------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|-------|-------------------|
| text                      | text that will be compared with the vector's textual elements                                                                                                                                     | str   | ''                |
| text_vector               | vector of strings with the elements of the comparison                                                                                                                                             | list  | []                |
| minimum_instruction_score | minimum percentage of similarity of the input text with the beginning of the closest element, if reached the beginning of the response text will be removed up to the first punctuation character | int   | 3                 |

### semanticMethod (function return type: dict): Returns a dictionary with the metrics of the vector of a matrix that is closest to the input vector, using a semantic algorithm.
Parameters
| Name                      | Description                                                                                                                                                                                       | Type  | Default Value     |
|---------------------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|-------|-------------------|
| vector                    | vector that will be compared to the vector elements of the matrix                                                                                                                                 | list  | []                |
| matrix                    | matrix that will have its vectors compared to the input vector                                                                                                                                    | list  | []                |
| removes_completeness      | removes the numeric elements that have been inserted to complete the size of the vector                                                                                                           | bool  | True              |

### euclideanMethod (function return type: dict): Returns a dictionary with the metrics of the vector of a matrix that is closest to the input vector, using a euclidean algorithm.
Parameters
| Name                      | Description                                                                                                                                                                                       | Type  | Default Value     |
|---------------------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|-------|-------------------|
| vector                    | vector that will be compared to the vector elements of the matrix                                                                                                                                 | list  | []                |
| matrix                    | matrix that will have its vectors compared to the input vector                                                                                                                                    | list  | []                |
| removes_completeness      | removes the numeric elements that have been inserted to complete the size of the vector                                                                                                           | bool  | True              |

### semanticComparison (function return type: float): Returns the percentage level of similarity between two strings.
Parameters
| Name                      | Description                                                                                                                                                                                       | Type  | Default Value     |
|---------------------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|-------|-------------------|
| string1                   | first string that will be compared to the second string                                                                                                                                           | str   | ''                |
| string2                   | second string that will be compared to the first string                                                                                                                                           | str   | ''                |

### outputAdaptedToInput (function return type: str/generator object): Returns the output text adapted to the semantics of the input text.
Parameters
| Name                      | Description                                                                                                                                                                                       | Type  | Default Value     |
|---------------------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|-------|-------------------|
| Input                     | input text, which will have its patterns transferred to the output text                                                                                                                           | str   | ''                |
| Output                    | output text, which will receive the patterns assimilated from the input text                                                                                                                      | str   | ''                |
| hot                       | if True returns the output text adapted to the input text, if False just returns the original output text                                                                                         | bool  | True              |
| stream                    | if True returns the result token by token as each token is generated, if False joins the tokens in memory and returns them all at once in string format                                           | bool  | False             |

### embeddingForText (function return type: str): Returns a vector of embeddings converted to text.
Parameters
| Name                      | Description                                                                                                                                                                                       | Type  | Default Value     |
|---------------------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|-------|-------------------|
| embedding                 | numeric list that has previously been converted from text to a vector of embeddings                                                                                                               | list  | []                |
| tokenizer                 | algorithm of tokenizer used to transform the original text into an embeddings vector                                                                                                              | str   | 'sapi'            |

### addHiddenLayer (function return type: bool): Returns True if a hidden layer is successfully added to the network architecture, or False otherwise.
Parameters
| Name                      | Description                                                                                                                                                                                       | Type  | Default Value     |
|---------------------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|-------|-------------------|
| num_neurons               | number of neurons that the hidden layer that is being built will have                                                                                                                             | int   | 0                 |

### train (function return type: bool): Returns True if the neural network training is successful, or False otherwise.
Parameters
| Name                      | Description                                                                                                                                                                                       | Type  | Default Value     |
|---------------------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|-------|-------------------|
| dataset_path              | local path or a web path to a file in text or json format that will be used as the data source for training the model                                                                             | str   | ''                |
| string                    | text with all training data or with data to complement the content of the text/json file                                                                                                          | str   | ''                |
| precision                 | percentage relative to the amount of characters that will remain in each word or token, if it is less than 1.0 the characters to the right of each word or token will be removed                  | float | 1.0               |
| tokenizer                 | algorithm for text tokenization, can be 'gpt' for the standard algorithm that is used in most language models, or 'sapi' for the algorithm created by sapiens technology                          | str   | 'gpt'             |
| method                    | training method, where each type of method will apply a different calculation in the training and inference of the model                                                                          | str   | 'semantic'        |
| interaction               | if True enables the hurnet network interaction calculus to abstract more complex patterns, if False does not use the hurnet network interaction calculus (calculation with False is more faster)  | bool  | True              |
| activation_function       | activation function to be used in non-linear patterns: 'linear', 'sigmoid', 'tanh', 'relu', 'leaky_relu', 'softmax', 'softplus', 'elu', 'silu', 'swish', 'gelu', 'selu', 'mish' or 'hard_sigmoid' | str   | 'linear'          |
| bias                      | number of bias added to the network calculation to force results up or down                                                                                                                       | float | 0.0               |
| learning_rate             | multiplier factor for the hurnet network's learning pace, should be neither too high nor too low                                                                                                  | float | 1.0               |
| stochastic_factor         | if True adds indeterminism to the calculation with random values to the network weights, if False remains with the original weights                                                               | bool  | False             |
| fx                        | if True uses the improved calculation for feature expansion that abstracts more subtle patterns, if False assumes that the training data contains only noticeable patterns                        | bool  | False             |
| progress                  | if True enables the progress bar that displays the current stage of training, if False will hide the progress bar                                                                                 | bool  | True              |

### saveModel (function return type: bool): Returns True if the model is saved successfully, or False otherwise.
Parameters
| Name                      | Description                                                                                                                                                                                       | Type  | Default Value     |
|---------------------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|-------|-------------------|
| model_path                | local path to the directory where the model should be generated, followed by the name used for the model files                                                                                    | str   | ''                |
| progress                  | if True enables the progress bar that displays the current stage of saving, if False will hide the progress bar                                                                                   | bool  | True              |

### loadModel (function return type: bool): Returns True if the model is loaded successfully, or False otherwise.
Parameters
| Name                      | Description                                                                                                                                                                                       | Type  | Default Value     |
|---------------------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|-------|-------------------|
| model_path                | path to the directory where the model files are located, optionally followed by the name of the files in the directory, or by the name of the scnnet or hurnet file                               | str   | ''                |
| progress                  | if True enables the progress bar that displays the current stage of loading, if False will hide the progress bar                                                                                  | bool  | True              |

### addFit (function return type: bool): Returns True if an of "input/prompt/question" and "output/answer" pair is successfully added to the current model, or False otherwise.
Parameters
| Name                      | Description                                                                                                                                                                                       | Type  | Default Value     |
|---------------------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|-------|-------------------|
| prompt                    | input text for a given response to be obtained                                                                                                                                                    | str   | ''                |
| answer                    | response to be returned when the input is sent for model prediction                                                                                                                               | str   | ''                |

### predict (function return type: str/generator object): Returns a string with the response to the user prompt.
Parameters
| Name                      | Description                                                                                                                                                                                       | Type  | Default Value     |
|---------------------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|-------|-------------------|
| prompt                    | text with the question, request or instruction for the model                                                                                                                                      | str   | ''                |
| minimum_score             | minimum percentage of reliability in the response for it to be returned in the prediction, if the reliability is less than this value an empty string will be returned                            | float | 0.5               |
| hot                       | if True will vary the response and/or adapt the response to the user's question, if False will return exactly the same response as the training                                                   | bool  | False             |
| stream                    | if True it will return a generator object with one token at a time as the tokens are generated, if False it will return the full text only after all the tokens have been generated               | bool  | False             |

### print_predict (method without return): Displays a string with the model prediction result.
Parameters
| Name                      | Description                                                                                                                                                                                       | Type  | Default Value     |
|---------------------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|-------|-------------------|
| prompt                    | text with the question, request or instruction for the model                                                                                                                                      | str   | ''                |
| minimum_score             | minimum percentage of reliability in the response for it to be displayed in the prediction, if the reliability is less than this value an empty string will be displayed                          | float | 0.5               |
| hot                       | if True will vary the response and/or adapt the response to the user's question, if False will disply exactly the same response of training                                                       | bool  | False             |
| stream                    | if True will display one token at a time as the tokens are being generated, if False it will display the full text only after all the tokens have been generated                                  | bool  | False             |

Check out now a comparison between a conventional Transformer architecture model and our semantic comparison architecture with HurNet.
```bash
pip install torch tiktoken
```
```python
# this is a code of a transformer algorithm for gpt models; it belongs to sapiens technology® and its unauthorized use by third parties is strictly prohibited
# !pip install torch tiktoken or !pip install torch==2.4.1 and then !pip install tiktoken==0.4.0
class GPTModel: # main class for a standard pre-trained generative transformer model
    def __init__(self): # gpt model architecture builder
        from torch.utils.data import Dataset, DataLoader
        from torch import nn, triu, ones
        from torch.nn import Module, functional as F, utils
        from torch import no_grad, tensor, int64, multinomial, cat, save, load
        from json import load as json_load
        from tiktoken import get_encoding
        from torch import optim
        from tqdm import tqdm
        from os import path as os_path, makedirs as os_makedirs
        from torch import cuda, device, backends        
        if cuda.is_available(): local_device = device('cuda')
        elif backends.mps.is_available(): local_device = device('mps')
        else: local_device = device('cpu')
        self.__Dataset = Dataset
        self.__Module = Module
        self.__nn = nn
        self.__tensor = tensor
        self.__triu = triu
        self.__ones = ones
        self.__no_grad = no_grad
        self.__device = local_device
        self.__F = F
        self.__int64 = int64
        self.__multinomial = multinomial
        self.__cat = cat
        self.__json_load = json_load
        self.__get_encoding = get_encoding
        self.__DataLoader = DataLoader
        self.__optim = optim
        self.__utils = utils
        self.__tqdm = tqdm
        self.__os_path = os_path
        self.__os_makedirs = os_makedirs
        self.__save = save
        self.__load = load
        self.__model = None
        self.__encode = None
        self.__block_size = 500
        self.__decode = None
        self.__string = ''
        self.__vocab_size = 0
        self.__char_to_idx = {}
        self.__idx_to_char = {}
        self.__tokenizer = 'sapi'
        self.__batch_size = 32
        self.__embedding_dim = 384
        self.__number_heads = 6
        self.__number_layers = 6
        self.__dropout = 0.1
        self.__optimizer = None
        self.__learning_rate = 3e-4
        self.__eval_interval = 500
        self.__train = False
        self.parameters_number = 0
        class TextDataset(self.__Dataset): # class for processing training data
            def __init__(self, data={}, block_size=0): self.data, self.block_size = data, block_size
            def __len__(self): return len(self.data) - self.block_size
            def __getitem__(self, index=0):
                input_sequence = self.data[index:index + self.block_size]
                target_sequence = self.data[index + 1:index + self.block_size + 1]
                return input_sequence, target_sequence
        self.__TextDataset = TextDataset
        class Transformer(self.__Module): # building transformer architecture
            def __init__(self, outer=None, vocab_size=0, embedding_dim=0, number_heads=0, number_layers=0, dropout=None, block_size=0):
                super().__init__()
                self.outer = outer
                self.embedding = outer._GPTModel__nn.Embedding(vocab_size, embedding_dim)
                self.pos_encoder = outer._GPTModel__nn.Parameter(outer._GPTModel__tensor([]).new_zeros(1, block_size, embedding_dim))
                self.transformer = outer._GPTModel__nn.TransformerDecoder(outer._GPTModel__nn.TransformerDecoderLayer(d_model=embedding_dim, nhead=number_heads, dropout=dropout), num_layers=number_layers)
                self.fc_out = outer._GPTModel__nn.Linear(embedding_dim, vocab_size)
                self.dropout = outer._GPTModel__nn.Dropout(dropout)
                self.block_size = block_size
            def forward(self, input_tensor=[]):
                outer = self.outer
                batch_size, seq_len = input_tensor.size()
                positions = self.pos_encoder[:, :seq_len, :].to(input_tensor.device)
                embedded = self.dropout(self.embedding(input_tensor) + positions)
                transposed = embedded.transpose(0, 1)
                mask = outer._GPTModel__triu(outer._GPTModel__ones(seq_len, seq_len, device=input_tensor.device) * float('-inf'), diagonal=1)
                output = self.transformer(transposed, transposed, tgt_mask=mask)
                output = output.transpose(0, 1)
                return self.fc_out(output)
        self.__Transformer = Transformer
    def __compute_loss(self, loader=[]): # function for computing network loss rate
        self.__model.eval()
        total_loss = 0
        with self.__no_grad():
            for input_batch, target_batch in loader:
                input_batch, target_batch = input_batch.to(self.__device), target_batch.to(self.__device)
                logits = self.__model(input_batch)
                loss = self.__F.cross_entropy(logits.view(-1, logits.size(-1)), target_batch.view(-1))
                total_loss += loss.item()
        return total_loss / len(loader)
    def __format_params(self, number_params=0): # function for formatting the number of network parameters
        if number_params < 1_000_000: return f'{number_params}P'
        elif number_params < 1_000_000_000: return f'{number_params // 1_000_000}M'
        elif number_params < 1_000_000_000_000: return f'{number_params // 1_000_000_000}B'
        else: return f'{number_params // 1_000_000_000_000}T'
    def __generate_tokens(self, prompt='', max_tokens=500, temperature=1.0): # function to generate the predicted tokens in the inference
        self.__model.eval()
        encoded_prompt = self.__encode(prompt)
        input_tensor = self.__tensor(encoded_prompt, dtype=self.__int64).unsqueeze(0).to(self.__device)
        with self.__no_grad():
            tokens_generated = 0
            while True:
                conditioned_input = input_tensor[:, -self.__block_size:] if input_tensor.size(1) > self.__block_size else input_tensor
                logits = self.__model(conditioned_input)
                logits = logits[:, -1, :] / temperature
                probs = self.__F.softmax(logits, dim=-1)
                next_token = self.__multinomial(probs, num_samples=1)
                input_tensor = self.__cat((input_tensor, next_token), dim=1)
                token = next_token.item()
                decoded_token = self.__decode([token])
                if tokens_generated == 0 and '\n' in decoded_token: continue
                tokens_generated += 1
                yield decoded_token
                if (tokens_generated >= max_tokens and decoded_token[-1] in {'.', '\n', '!', '?', ';'}) or (tokens_generated >= (max_tokens*2)): break
    def train(self, dataset_path='', tokenizer='sapi', precision=0.5, context_window=500, progress=True): # function for training a conventional transformer model
        try:
            """
                Arguments:
                    dataset_path: receives a string with the address of a txt or json file for model training  
                    tokenizer: receives a string with the value 'sapi' to use sapiens' tokenizer, or 'gpt' to use the generative pre-trained transformer tokenizer  
                    precision: receives a float with a target value for the precision of weights adjustment in backpropagation; backpropagation will only stop if this target is reached  
                    context_window: receives an integer with the limit for the context window to be created for the model  
                    progress: receives a boolean indicating whether the progress bar will be displayed or hidden  
            """
            dataset_path = str(dataset_path).strip()
            tokenizer = str(tokenizer).lower().strip()
            precision = float(precision) if type(precision) in (bool, int, float) else 0.5
            context_window = max((1, int(context_window))) if type(context_window) in (bool, int, float) else 500
            progress = bool(progress) if type(progress) in (bool, int, float) else True
            self.__block_size = context_window
            loss_limit = max(0, min(1, 1 - precision))
            is_txt, is_json, formatted_sequences = dataset_path.endswith('.txt'), dataset_path.endswith('.json'), []
            if not is_txt and not is_json: raise ValueError('Unsupported file format. Use .txt or .json')
            if is_txt:
                with open(dataset_path, 'r', encoding='utf-8') as file: text_data = file.read()
            elif is_json:
                with open(dataset_path, 'r', encoding='utf-8') as file: json_data = self.__json_load(file)
                if type(json_data) == dict:
                    data_key = list(json_data.keys())[0]
                    pairs = json_data[data_key]
                else: pairs = json_data
                formatted_sequences = [str(pair[list(pair.keys())[0]]+'\n'+pair[list(pair.keys())[1]]).strip() for pair in pairs]
                text_data = '\n\n'.join(formatted_sequences)
            if len(self.__string) > 0: text_data += '\n\n'+self.__string
            text_data = text_data.strip()
            if tokenizer == 'sapi':
                chars = sorted(list(set(text_data)))
                self.__vocab_size = len(chars)
                self.__char_to_idx = {char: index for index, char in enumerate(chars)}
                self.__idx_to_char = {index: char for index, char in enumerate(chars)}
                self.__encode = lambda string: [self.__char_to_idx[char] for char in string]
                self.__decode = lambda indices: ''.join([self.__idx_to_char[index] for index in indices])
            else:
                encode = self.__get_encoding('gpt2')
                self.__vocab_size = encode.n_vocab
                self.__encode = encode.encode
                self.__decode = encode.decode
            data = self.__tensor(self.__encode(text_data), dtype=self.__int64)
            split_point = int(0.9 * len(data))
            train_data = data[:split_point]
            val_data = data[split_point:]
            if len(train_data) < self.__block_size:
                if len(train_data) > 1: self.__block_size = len(train_data) - 1
                else: raise ValueError('Dataset too small for training. Add more data.')
            self.__tokenizer = tokenizer
            train_dataset = self.__TextDataset(train_data, self.__block_size)
            val_dataset = self.__TextDataset(val_data, self.__block_size)
            train_loader = self.__DataLoader(train_dataset, batch_size=self.__batch_size, shuffle=True)
            val_loader = self.__DataLoader(val_dataset, batch_size=self.__batch_size, shuffle=False)
            self.__model = self.__Transformer(self, self.__vocab_size, self.__embedding_dim, self.__number_heads, self.__number_layers, self.__dropout, self.__block_size).to(self.__device)
            self.__optimizer = self.__optim.AdamW(self.__model.parameters(), lr=self.__learning_rate)
            scheduler = self.__optim.lr_scheduler.ReduceLROnPlateau(self.__optimizer, mode='min', factor=0.5, patience=3)
            epoch, step, best_val_loss = 0, 0, float('inf')            
            while True:
                self.__model.train()
                total_train_loss = 0
                str_epoch = str(epoch+1).rjust(10, '0')
                for input_batch, target_batch in train_loader:
                    input_batch, target_batch = input_batch.to(self.__device), target_batch.to(self.__device)
                    logits = self.__model(input_batch)
                    loss = self.__F.cross_entropy(logits.view(-1, logits.size(-1)), target_batch.view(-1))
                    self.__optimizer.zero_grad()
                    loss.backward()
                    self.__utils.clip_grad_norm_(self.__model.parameters(), 1.0)
                    self.__optimizer.step()
                    total_train_loss += loss.item()
                    if step > 0 and step % self.__eval_interval == 0:
                        val_loss = self.__compute_loss(val_loader)
                        scheduler.step(val_loss)
                        if val_loss < best_val_loss: best_val_loss = val_loss
                    step += 1
                avg_train_loss = total_train_loss / len(train_loader)
                if avg_train_loss <= loss_limit:
                    if progress: print()
                    break
                elif progress:
                    format_str = '{desc}: {percentage:3.0f}%|{bar:10}| {n_fmt}/{total_fmt} [{elapsed}<{remaining}, {rate_fmt}]'
                    current_precision = max(0, min(1, 1 - avg_train_loss))
                    str_current_precision = f'{current_precision:.4f}'.ljust(5, '0')
                    str_precision = f'{precision:.4f}'.ljust(5, '0')
                    train_loader = self.__tqdm(train_loader, desc=f'Epoch {str_epoch} - current precision is {str_current_precision}; aiming for precision >= {str_precision} in training', bar_format=format_str)
                epoch += 1
            return True
        except Exception as error:
            print('ERROR in train: ' + str(error))
            return False
    def saveModel(self, model_path='', progress=True): # function to save a pre-trained model
        try:
            """
                Arguments:
                    model_path: receives a string with the address and name of the model file to be generated  
                    progress: receives a boolean indicating whether the progress bar will be displayed or hidden  
            """
            model_path = str(model_path).strip()
            progress = bool(progress) if type(progress) in (bool, int, float) else True
            if self.__model is None: raise ValueError('Model is not initialized. Call train or loadModel first.')
            number_params = sum(p.numel() for p in self.__model.parameters())
            formatted_params = self.__format_params(number_params)
            if isinstance(model_path, str):
                directory, file_name = self.__os_path.split(model_path)
                if not file_name: file_name = 'model.gpt'
                elif not file_name.endswith('.gpt'): file_name += '.gpt'
            else: directory, file_name = str(model_path), 'model.gpt'
            if directory and not self.__os_path.exists(directory): self.__os_makedirs(directory)
            save_path = self.__os_path.join(directory, file_name)
            save_dict = {'model_state_dict': self.__model.state_dict(), 'tokenizer': self.__tokenizer, 'vocab_size': self.__vocab_size, 'block_size': self.__block_size}
            if self.__tokenizer == 'sapi': save_dict['char_to_idx'], save_dict['idx_to_char'] = self.__char_to_idx, self.__idx_to_char
            if progress:
                for _ in self.__tqdm(range(10), desc=f'Saving model with {formatted_params} parameters', leave=False): self.__save(save_dict, save_path)
            else: self.__save(save_dict, save_path)
            self.__train = True
            return True
        except Exception as error:
            print('ERROR in saveModel: ' + str(error))
            return False
    def loadModel(self, model_path='', progress=True): # function to load a previously saved pre-trained model
        try:
            """
                Arguments:
                    model_path: receives a string with the address and name of the model file to be loaded  
                    progress: receives a boolean indicating whether the progress bar will be displayed or hidden  
            """
            model_path = str(model_path).strip()
            progress = bool(progress) if type(progress) in (bool, int, float) else True
            if len(model_path) > 0:
                directory, file_name = self.__os_path.split(model_path)
                if not file_name: file_name = 'model.gpt'
                elif not file_name.endswith('.gpt'): file_name += '.gpt'
            else: directory, file_name = str(model_path), 'model.gpt'
            model_file = self.__os_path.join(directory, file_name)
            if progress:
                for _ in self.__tqdm(range(10), desc='Loading model', leave=False): checkpoint = self.__load(model_file, map_location=self.__device)
            else: checkpoint = self.__load(model_file, map_location=self.__device)
            self.__tokenizer = checkpoint['tokenizer']
            self.__vocab_size = checkpoint['vocab_size']
            self.__block_size = checkpoint['block_size']
            if self.__tokenizer == 'sapi':
                self.__char_to_idx = checkpoint['char_to_idx']
                self.__idx_to_char = checkpoint['idx_to_char']
                self.__encode = lambda string: [self.__char_to_idx[char] for char in string]
                self.__decode = lambda indices: ''.join([self.__idx_to_char[index] for index in indices])
            else:
                encode = self.__get_encoding('gpt2')
                self.__encode = encode.encode
                self.__decode = encode.decode
            self.__model = self.__Transformer(self, self.__vocab_size, self.__embedding_dim, self.__number_heads, self.__number_layers, self.__dropout, self.__block_size).to(self.__device)
            self.__model.load_state_dict(checkpoint['model_state_dict'])
            number_params = sum(p.numel() for p in self.__model.parameters())
            self.parameters_number, self.__optimizer, self.__train = number_params, None, True
            return True
        except Exception as error:
            print('ERROR in loadModel: ' + str(error))
            return False
    def addFit(self, prompt='', answer=''): # function to add fine-tuning to a dataset before training, or to a previously loaded model
        try:
            """
                Arguments:
                    prompt: receives a string with the input sample to be added to the current model  
                    answer: receives a string with the output sample to be added to the current model  
            """
            prompt = str(prompt).strip()
            answer = str(answer).strip()
            if not self.__train: self.__string += prompt+'\n'+answer+'\n\n'
            else:
                if self.__model is None: raise ValueError('Model is not initialized. Call train or loadModel first.')
                if self.__optimizer is None: self.__optimizer = self.__optim.AdamW(self.__model.parameters(), lr=self.__learning_rate)
                formatted = prompt+'\n'+answer+'\n\n'
                encoded = self.__encode(formatted)
                if len(encoded) > self.__block_size: encoded = encoded[:self.__block_size]
                input_tensor = self.__tensor(encoded[:-1], dtype=self.__int64).unsqueeze(0).to(self.__device)
                target_tensor = self.__tensor(encoded[1:], dtype=self.__int64).unsqueeze(0).to(self.__device)
                self.__model.train()
                logits = self.__model(input_tensor)
                loss = self.__F.cross_entropy(logits.view(-1, logits.size(-1)), target_tensor.view(-1))
                self.__optimizer.zero_grad()
                loss.backward()
                self.__utils.clip_grad_norm_(self.__model.parameters(), 1.0)
                self.__optimizer.step()
            return True
        except Exception as error:
            print('ERROR in addFit: ' + str(error))
            return False
    def predict(self, prompt='', max_tokens=500, stream=False): # function to return the inference result
        try:
            """
                Arguments:
                    prompt: receives a string with the input for which an output is desired  
                    max_tokens: receives an integer with an approximate number for the maximum tokens to be generated in the response  
                    stream: receives a boolean indicating whether the response will be returned token by token or all at once  
            """
            prompt = str(prompt).strip()
            max_tokens = max((1, int(max_tokens))) if type(max_tokens) in (bool, int, float) else 500
            stream = bool(stream) if type(stream) in (bool, int, float) else False
            if self.__model is None: raise ValueError('Model is not initialized. Call train or loadModel first.')
            if stream: return self.__generate_tokens(prompt, max_tokens)
            tokens = list(self.__generate_tokens(prompt, max_tokens))
            return ''.join(tokens)
        except Exception as error:
            print('ERROR in predict: ' + str(error))
            return ''
    def print_predict(self, prompt='', max_tokens=500, stream=False): # method to display the inference result
        try:
            """
                Arguments:
                    prompt: receives a string with the input for which an output is desired  
                    max_tokens: receives an integer with an approximate number for the maximum tokens to be generated in the response  
                    stream: receives a boolean indicating whether the response will be displayed token by token or all at once  
            """
            prompt = str(prompt).strip()
            max_tokens = max((1, int(max_tokens))) if type(max_tokens) in (bool, int, float) else 500
            stream = bool(stream) if type(stream) in (bool, int, float) else False
            if self.__model is None: raise ValueError('Model is not initialized. Call train or loadModel first.')
            if stream:
            	[print(token, end='', flush=True) for token in self.__generate_tokens(prompt, max_tokens)]
            	print()
            else: print(self.predict(prompt, stream=False))
        except Exception as error:
            print('ERROR in print_predict: ' + str(error))
# this is a code of a transformer algorithm for gpt models; it belongs to sapiens technology® and its unauthorized use by third parties is strictly prohibited

```
```python
with open('./dataset.txt', 'r', encoding='utf-8') as file: content = file.read() # reading the contents of the text file
from semantic_comparison_network import SemanticComparisonNetwork # import the semantic neural network class
count_tokens = SemanticComparisonNetwork().countTokens(text=content) # counts the number of tokens in the training dataset
print(f'The current dataset has {count_tokens} tokens.') # displays the total number of tokens in the current dataset

```
```bash
The current dataset has 451 tokens.
```
```python
# ---> insert here the code of the GPTModel class defined above...
from time import time # import time module
start = time() # marks the initial time

transformer = GPTModel() # instantiation of the transformer class for the gpt model
# training the model with a text-based dataset using the gpt tokenizer and achieving 97% accuracy with a context window of 200 tokens
transformer.train(dataset_path='./dataset.txt', tokenizer='gpt', precision=0.97, context_window=200, progress=True)
transformer.saveModel(model_path='./transformer_model.gpt', progress=True) # saving the pre-trained generative model

end = time() # marks the end time
time_spent_transformer = abs(start-end) # calculates the time difference between the start and end of execution
print(f'\nRuntime: {time_spent_transformer} seconds.') # displays the total time spent in seconds

```
Runned on a Macbook M3 Max with 48GB of VRAM.
```bash
Epoch 0000000001 - current precision is 0.0000; aiming for precision >= 0.9700 in training: 100%|██████████| 8/8 [00:02<00:00,  3.31it/s]
Epoch 0000000002 - current precision is 0.0000; aiming for precision >= 0.9700 in training: 100%|██████████| 8/8 [00:02<00:00,  3.33it/s]
Epoch 0000000003 - current precision is 0.0000; aiming for precision >= 0.9700 in training: 100%|██████████| 8/8 [00:02<00:00,  3.33it/s]
Epoch 0000000004 - current precision is 0.0000; aiming for precision >= 0.9700 in training: 100%|██████████| 8/8 [00:02<00:00,  3.33it/s]
Epoch 0000000005 - current precision is 0.0000; aiming for precision >= 0.9700 in training: 100%|██████████| 8/8 [00:02<00:00,  3.29it/s]
Epoch 0000000006 - current precision is 0.0805; aiming for precision >= 0.9700 in training: 100%|██████████| 8/8 [00:02<00:00,  3.32it/s]
Epoch 0000000007 - current precision is 0.3691; aiming for precision >= 0.9700 in training: 100%|██████████| 8/8 [00:02<00:00,  3.32it/s]
Epoch 0000000008 - current precision is 0.5436; aiming for precision >= 0.9700 in training: 100%|██████████| 8/8 [00:02<00:00,  3.32it/s]
Epoch 0000000009 - current precision is 0.6632; aiming for precision >= 0.9700 in training: 100%|██████████| 8/8 [00:02<00:00,  3.32it/s]
Epoch 0000000010 - current precision is 0.7398; aiming for precision >= 0.9700 in training: 100%|██████████| 8/8 [00:02<00:00,  3.32it/s]
Epoch 0000000011 - current precision is 0.8036; aiming for precision >= 0.9700 in training: 100%|██████████| 8/8 [00:02<00:00,  3.31it/s]
Epoch 0000000012 - current precision is 0.8394; aiming for precision >= 0.9700 in training: 100%|██████████| 8/8 [00:02<00:00,  3.30it/s]
Epoch 0000000013 - current precision is 0.8418; aiming for precision >= 0.9700 in training: 100%|██████████| 8/8 [00:02<00:00,  3.28it/s]
Epoch 0000000014 - current precision is 0.8710; aiming for precision >= 0.9700 in training: 100%|██████████| 8/8 [00:02<00:00,  3.23it/s]
Epoch 0000000015 - current precision is 0.8941; aiming for precision >= 0.9700 in training: 100%|██████████| 8/8 [00:02<00:00,  3.19it/s]
Epoch 0000000016 - current precision is 0.9130; aiming for precision >= 0.9700 in training: 100%|██████████| 8/8 [00:02<00:00,  3.16it/s]
Epoch 0000000017 - current precision is 0.9259; aiming for precision >= 0.9700 in training: 100%|██████████| 8/8 [00:02<00:00,  3.14it/s]
Epoch 0000000018 - current precision is 0.9359; aiming for precision >= 0.9700 in training: 100%|██████████| 8/8 [00:02<00:00,  3.14it/s]
Epoch 0000000019 - current precision is 0.9457; aiming for precision >= 0.9700 in training: 100%|██████████| 8/8 [00:02<00:00,  3.15it/s]
Epoch 0000000020 - current precision is 0.9542; aiming for precision >= 0.9700 in training: 100%|██████████| 8/8 [00:02<00:00,  3.16it/s]
Epoch 0000000021 - current precision is 0.9616; aiming for precision >= 0.9700 in training: 100%|██████████| 8/8 [00:02<00:00,  3.17it/s]
Epoch 0000000022 - current precision is 0.9656; aiming for precision >= 0.9700 in training: 100%|██████████| 8/8 [00:02<00:00,  3.18it/s]
Epoch 0000000023 - current precision is 0.9700; aiming for precision >= 0.9700 in training: 100%|██████████| 8/8 [00:02<00:00,  3.19it/s]

                                                                                                                                                                                 
Runtime: 63.26045322418213 seconds.
```
```python
from time import time # import time module
start = time() # marks the initial time

from semantic_comparison_network import SemanticComparisonNetwork # import of the module semantic class
scnet = SemanticComparisonNetwork() # instantiation of the semantic class for the scnet model
# training the model with a text-based dataset using the gpt tokenizer and achieving 97% accuracy with a infinity context window
scnet.train(dataset_path='./dataset.txt', tokenizer='gpt', precision=0.97, progress=True)
scnet.saveModel(model_path='./scnet_model/scnet_file', progress=True) # saving the pre-trained generative model

end = time() # marks the end time
time_spent_scnet = abs(start-end) # calculates the time difference between the start and end of execution
print(f'\nRuntime: {time_spent_scnet} seconds.') # displays the total time spent in seconds

```
Runned on a Macbook M3 Max with 48GB of VRAM.
The **SCNet** network was **326 times** faster in training than a conventional Transformer network using the same dataset.
```bash
Converting text: 100%|██████████████████████████████████████████████████████████████████████████████████████████████████████████████████| 2362/2362 [00:00<00:00, 3795764.77it/s]
Structuring data: 100%|███████████████████████████████████████████████████████████████████████████████████████████████████████████████████████| 11/11 [00:00<00:00, 87216.15it/s]
Semantic model training: 100%|█████████████████████████████████████████████████████████████████████████████████████████████████████████████████████| 7/7 [00:00<00:00, 51.30it/s]
Tokenizing data: 100%|██████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████| 11/11 [00:00<00:00, 141.29it/s]
Saving semantic model: 100%|████████████████████████████████████████████████████████████████████████████████████████████████████████████████████| 7/7 [00:00<00:00, 13113.05it/s]

Runtime: 0.19397306442260742 seconds.
```
Now see an inference test with the generated models.
```python
# ---> insert here the code of the GPTModel class defined above...
from time import time # import time module
start = time() # marks the initial time

transformer = GPTModel() # instantiation of the transformer class for the gpt model
transformer.loadModel(model_path='./transformer_model.gpt', progress=True) # loading the pre-trained generative model

prompt = 'What are the main types of machine learning?' # prompt for inference test
transformer.print_predict(prompt=prompt, max_tokens=50, stream=True) # infers token by token up to approximately 50 tokens

end = time() # marks the end time
time_spent_transformer = abs(start-end) # calculates the time difference between the start and end of execution
print(f'\nRuntime: {time_spent_transformer} seconds.') # displays the total time spent in seconds

```
Runned on a Macbook M3 Max with 48GB of VRAM.
```bash
The three main types are:                                                                                                                                                        
- **Supervised Learning**: The model learns from labeled data;
- **Unsupervised Learning**: The model identifies patterns without labels;
- **Reinforcement Learning**: The model learns through trial and error, receiving rewards or penalties;

Runtime: 4.319222927093506 seconds.
```
```python
from time import time # import time module
start = time() # marks the initial time

from semantic_comparison_network import SemanticComparisonNetwork # import of the module semantic class
scnet = SemanticComparisonNetwork() # instantiation of the semantic class for the scnet model
scnet.loadModel(model_path='./scnet_model/scnet_file', progress=True) # loading the pre-trained generative model

prompt = 'What are the main types of machine learning?' # prompt for inference test
scnet.print_predict(prompt=prompt, stream=True) # infers all required tokens one by one

end = time() # marks the end time
time_spent_scnet = abs(start-end) # calculates the time difference between the start and end of execution
print(f'\nRuntime: {time_spent_scnet} seconds.') # displays the total time spent in seconds

```
Runned on a Macbook M3 Max with 48GB of VRAM.
The **SCNet** network was **11 times** faster in inferring than a conventional Transformer network using the same dataset.
```bash
Loading semantic model: 100%|████████████████████████████████████████████████████████████████████████████████████████████████████████████████████| 7/7 [00:00<00:00, 6918.03it/s]
The three main types are: 
 - **Supervised Learning**: The model learns from labeled data; 
 - **Unsupervised Learning**: The model identifies patterns without labels; 
 - **Reinforcement Learning**: The model learns through trial and error, receiving rewards or penalties;

Runtime: 0.38736629486083984 seconds.
```

## Contributing

We do not accept contributions that may result in changing the original code.

Make sure you are using the appropriate version.

## License

This is proprietary software and its alteration and/or distribution without the developer's authorization is not permitted.
