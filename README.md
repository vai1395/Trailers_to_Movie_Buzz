# Trailers_to_Movie_Buzz
Welcome to our journey into the captivating realm of Movie Buzz, explored through YouTube trailers. In this exploration, I dive deep into understanding trailer perceptions, employing advanced BERT-based topic modeling and the powerful analysis of Llama2 to categorize these snippets into distinct groups.

Our main goal? To unravel the intricate tapestry of emotions underlying successful trailer creation. Trailers act as cinematic appetizers, offering previews of forthcoming movies. But how do viewers perceive these glimpses? My aim is to decode the various lenses through which people interpret trailers. Utilizing sophisticated BERT-based topic modeling techniques, I strive to cluster these trailers, identifying common captivating themes and elements.

Successful trailers go beyond visual stimulation, possessing a unique emotional resonance that captivates audiences. My analysis focuses on decoding the emotional spectrum prevalent in these previews to uncover the key ingredients contributing to their success. From excitement to suspense, joy to anticipation, my analysis aims to identify and understand the emotions that deeply resonate with viewers, ultimately defining a trailer's efficacy.

Analyzing these trailers starts with a comprehensive examination using Microsoft's Azure AI Video Indexer. This tool becomes my gateway to unlock valuable insights hidden within the trailers. The AI offers a plethora of functionalities and insights concerning video content, providing details about recognized individuals, discussed subjects, keywords, emotional cues, sentiments expressed, pivotal scenes, and more.

The information about specific videos is returned in a JSON file format, detailing the percentage representation of depicted sentiments and their positions within the content.

Moving on, I delve into sentiment distribution within the trailers. The metrics obtained from Azure AI Video Indexer help derive conclusive sentiment distributions. For instance, a higher identification of negative elements accentuates negativity within the trailer, while dominant positive sentiments amplify positivity.

Analyzing YouTube comments reveals the audience's reception and sentiment towards the trailer. This analysis, coupled with the volume of comments received, helps establish a buzz score, indicating the trailer's impact within the online community. This score, ranging from -5 to +5, contextualizes the trailer's reception, from minimal buzz to significant engagement and positive discussions.

Furthermore, utilizing the DeTour model, I employ advanced topic modeling techniques to synthesize trailer descriptions for further analysis. The Llama2 layer plays a pivotal role in generating comprehensive cluster descriptions and label names, showcasing its potential for enhanced accuracy.

In conclusion, my analysis showcases a strong correlation between diversified emotions in trailers and increased audience engagement. It emphasizes the importance of emotional balance, cautioning against over-reliance on singular emotions, while highlighting the impact of balanced sentiments for a larger viewership.

 More Details [here](https://medium.com/@nskp1990/trailer-sentiment-to-movie-buzz-524682ae25ce)
