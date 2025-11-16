from nltk.stem import PorterStemmer
from nltk.corpus import stopwords
import nltk
steamer=PorterStemmer()
paragraph = """ 

07 November 2025
01:15

Hello guys.
So we are going to continue our discussion with respect to Bag of Words.
Uh, already we have understood the intuition behind Bag of Words how it is converting a text into vectors.
Now, as usual, let's go ahead and discuss about the advantages and disadvantages.
So first of all, I will go ahead and write the advantages.
And then I will go ahead and write the disadvantages.
Okay.
So uh, and obviously we have also discussed about the advantages and disadvantages with respect to
one hot encoding.
We'll try to compare with this and we'll try to see that what all problems is getting fixed okay.
First of all yes.
Again uh this is easy to implement and it is intuitive.
So I will just write something like simple and intuitive.
Simple and.
Intuitive.
Okay.
The second point, uh, with respect to advantages.
Now here, what what we'll do in one hot encoding.
You, you see that we have seen that some important thing is there in machine learning algorithm.
Right.
Okay.
With respect to sparse matrix, I'll be discussing with respect to semantic meaning out of vocabulary
everything I'll be discussing.
First let's consider this particular second topic, which is like uh for ML algorithms we give fixed
size inputs.
Now over here with respect to bag of words.
Any statement.
Now here you can see that some of the sentence may be three words, five words, ten words.
At the end of the day, based on the vocabulary size, you are able to get all the sentences converted
into that many number of dimensions of words.
So here the vectors is getting fixed.
The inputs are getting fixed because here our vocabulary is getting fixed.
So this particular problem is getting solved okay.
In uh one hot encoding you do not have a fixed size inputs.
Since we are creating words for every vectors.
Sorry, we are creating vectors for every words.
Okay, so what we are going to do over here.
The second point that you will be seeing.
Yes you have a fixed size input.
Right.
And this is a superbly help you for ML algorithms training okay ML algorithms.
Now this is the two major advantages.
Now if I talk about the disadvantage see over here the first disadvantage with respect to one hot encoding
is sparse matrix.
And I've already told you what exactly sparse matrix it is.
Nothing but ones and zeros.
Let's say if your vocabulary size is 50,000, then what will happen?
Every sentence will get converted into you know that size of the vocabulary, right?
So still sparse matrix problem is there.
So with respect to disadvantage again I'm going to write it as sparse matrix and array.
Or array is still there and this will actually lead to overfitting.
Okay.
Now second major disadvantage again.
See, at the end of the day, whatever statement that you have like good boy, good girl, you know
or it can be boy girl good.
Okay.
Something like this.
You'll be seeing that based on this sentence.
Right.
And based on this vocabulary and based on the frequency of the vocabulary, the ordering of the word
is changing.
Now, see, understand if in a sentence the ordering of the word changes.
And based on that, this vector is getting created because, see, based on the frequency, we have
written all the vector, all the all the vocabularies right over here good was present maximum number
of times.
So we wrote it as first boy was present in the second number.
So we wrote it over here.
Right.
And a girl was present uh like two for two times.
And we have written it at last.
Right now over here, you can see that if I probably consider the third statement.
Boy, girl.
Good.
Right.
But here you can see that entire word is getting ordered like it is completely changed.
Right?
The ordering of the word is completely changed.
So I'm having 110 for sentence three.
I'm having 111.
Now.
When word ordering is changed, the meaning of the sentence is also gets changed.
And because of that, some of the semantic information is not getting captured.
I'll talk about more semantic information, but here you will be able to see that ordering of the words
is getting changed.
This is super important.
Ordering of the word is getting changed.
Because if this is getting changed, the meaning of the sentence is changes, right?
Is getting changed.
So this was the second disadvantage if I probably talk about the third disadvantage.
Okay.
Third disadvantage.
Again we'll go and see over here with respect to out of vocabulary.
Now what happens if I probably add a new word like boy girl good.
And let's say I'm going to add something called a school.
Now here you will be seeing that the school word is not present in the vocabulary.
So what it is going to do for this specific word anyhow?
It is going to get rejected, right?
It is.
It is not all getting considered in this training data.
Let's say that for our new test data, in our new test data, we have included a school word, and we
need to do the prediction for this particular word with respect to output.
So the first step will be that we will do text pre-processing.
And then we'll try to convert this into a bag of words using the same technique what we did in the training
data set.
But here you see that in my training data set I do not have a vocabulary which is called as school.
So what it is going to do, it is just going to ignore this specific word, and it is just going to
see that where good and boy and girl are there.
Right?
So still out of vocabulary still exists because this word may be an important word for the sentence,
but it is getting removed because we don't have that in the vocabulary.
Right?
Major problem.
So yes, out of vocabulary is obviously a issue over here.
Right.
This still persists.
Okay.
Oh.
Oh V mm.
Now this was the there.
Now one more important thing semantic meaning in this is still not being getting captured.
Why.
I'll tell you.
Semantic meaning.
Is still not getting captured.
And there are multiple things to explain in this.
Okay.
Now, first of all, obviously you know that I'm having either ones and zeros.
Okay.
Now in this particular case good.
And boy they are getting the same importance right.
For girl.
Obviously if the word is not present I'm getting zero.
Small amount of semantic information is getting captured when compared to the one hot encoding format.
But here you see that when we have many vocabularies, either my values will be ones or zeros.
One is just indicating whether the word is present or not, but which is the most important word?
What is the most important context in that particular sentence?
That is obviously not getting captured.
And if that is not getting captured, semantic in turn will not get captured.
Now, the other thing over here is that there is there is also very important thing.
Let's say that I'm having two sentences.
Okay.
It is like the food is good.
Let's say in my data set I have this sentence.
The food is not good.
Not good.
Now, let's say I don't go ahead and remove all the stop words and all.
For this I will be having a vocabulary like one.
Uh, one.
Let's say all these words are there, okay.
And there is also a separate, uh, vocabulary.
Food is also a separate vocabulary.
Is is also a separate how many unique vocabulary are there for because naught is also there.
Right.
So these will also become one, naught will be zero and good will be one.
Right.
So this is how we convert from this to this.
Right.
Similarly from here to here.
If I really need to convert then what it will happen 11111 because naught is also present.
So I'm writing one.
Now let's say this is my vector one and this is my vector two.
If I try to find out the difference or how similar this vector is just by plotting some points, let's
say that I've converted this particular dimension to two dimension using PC, and probably I've plotted
it based on this.
Right?
Only one value is getting changed is and not right.
So I will get both these vectors very much near to each other.
And this we can basically do it through something called as cosine similarity.
So let's say this is my vector one.
This is my vector one.
This is my vector two.
So vector one is basically present over here.
Vector two is present over here if it is near to each other, if the angle between them is very near
to each other, or if the angle between them is very less.
I may say that this both the sentences are same, almost same or similar, right?
This is almost similar.
But do you think this both sentences are almost similar because it is the complete opposite of them,
right?
But since there is only one word that is getting changed because of that only one, one of the value
is getting changed over here, right?
Like zeros and ones are happening.
And when we plot this, it is becoming kind of a kind of a similar word, but this should not be a similar
word.
This is completely opposite word.
Right.
So this kind of situation is also not getting handled well with the bag of words.
And later on the techniques that will be learning like uh, word two vec and all this will be solving
all these problems.
Right?
So I hope you are able to understand the advantages and disadvantages of Baggovut.
Super important with respect to interview and if your basics of this is getting strong, trust me you
will be able to understand bag of words average word two vec.
Sorry, you'll be able to understand word two vec average word to vec in a very easy manner.
And there are techniques in deep learning which is also going to come which is called as embedding techniques.
Word embedding and all all those will get solved in a very easy way.
Right.
So I hope you are able to understand this was with respect to the bag of words.
And now in the next video, what we are going to do is that we are going to do some practicals and we'll
try to see, with the help of sklearn how we can perform bag of words.
Right.
So yes, this was it from my side.
I will see you all in the next video.
Thank you."""
sentence=nltk.sent_tokenize(paragraph)
for i in range(len(sentence)):
    words=nltk.word_tokenize(sentence[i])
    words=[steamer.stem(word) for word in words if word not in set(stopwords.words("english"))]
    sentence[i]="".join(words)
    print(sentence[i])

from nltk.stem import WordNetLemmatizer
lemotizer=WordNetLemmatizer()

for i in range(len(sentence)):
    words=nltk.word_tokenize(sentence[i])
    words=[lemotizer.lemmatize(word) for word in words  if word not in set(stopwords.words("english" ))]
    sentence[i]="".join(words)
    print(sentence[i])