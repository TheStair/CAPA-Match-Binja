# CAPA-Match-Binja
Binary Ninja Plugin to Match Binaries to CAPA rules

**About This Project**
I took on this project with the goal of learning how to interface with a large pre-existing software project. I am totally new to the Binary Ninja API. As you can likely tell, this file will contain unused functions that I used to teach myself.

**Personal Goals for this project**
1. No Code from AI  
&nbsp;&nbsp;&nbsp;&nbsp; With the recent explosion of the trend of "*vibe coding*". I really want to take the time to sharpen up my fundamental programming skills.

2. Interface with a large pre-existing software project  
&nbsp;&nbsp;&nbsp;&nbsp; Learning to properly read documentation for APIs is a key skill, and something I really want to develop for my future self.

3. Increase my understanding of the Reverse-Engineering World  
&nbsp;&nbsp;&nbsp;&nbsp; With a career interest in Reverse-Engineering, Digital Forensics, and Incident Response, Learning Reverse-Engineering concepts and developing skills with RE tools, I can best prepare for my future career.  

**Challenges I faced**  
1. I initially faced challenges integrating binary ninja into my development environment, but I just had the wrong license. Additionally their linux install script made it super easy.   
2. Lack of flare-capa library documentation. This library appears to have very little useful public documentation. I think it's because they just expect you to use it as a standalone executable. 
3. Compute resources. Binary ninja analysis takes up a lot of RAM, and CAPA also loads the program into binja. On my laptop, after a certain size, CAPA fails to process the binary. For example, on my laptop files like /bin/ls or /bin/grep work, meanwhile /bin/bash for some reason is killed by the OS or python interpreter
