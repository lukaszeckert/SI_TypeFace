import sys

file_beginning = """


package com.sample
 
import javax.swing.*;

//declaring classes of object used in this project
declare Question
 	question : String 
	option1 : QuestionOption
	option2 : QuestionOption
	option3 : QuestionOption
end

declare QuestionOption
	option : String
end

declare QuestionAnswer
	question : Question
	answer : QuestionOption
end

//declaration of Gui helper functions
rule "Ask question"
	when 
		q: Question()
	then
		System.out.println(q.getQuestion());
		
		QuestionOption[] o;
		o = new QuestionOption[3];
		o[0] = q.getOption1();
		o[1] = q.getOption2();
		o[2] = q.getOption3();
		
		//Some options may by null
		int num_options = 2;
		for(;num_options>=0;num_options--)
		{
			if(o[num_options] !=null && o[num_options].getOption() != "")
				break;
		}
		num_options++;
		if(num_options == 0)
		{
			//Special case. Lets create dummy QuestionOption with OK text
			o[0] = new QuestionOption("OK");
			num_options = 1;
		}
		
		Object[] string_options = new Object[num_options];
		for(int i=0;i<num_options;++i)
			string_options[i] = (Object)o[i].getOption();
		
		 JFrame frame = new JFrame("DialogDemo");
        frame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        int n = JOptionPane.showOptionDialog(null, q.getQuestion(), "",
                JOptionPane.YES_NO_OPTION, JOptionPane.QUESTION_MESSAGE,
                null, string_options, string_options[0]);
        if(n!=-1)
        	insert( new QuestionAnswer(q,o[n]));
		else update(q);
end


//init statement 
//TODO move this to gui
rule "Init"
	when
	then
		insert(new QuestionAnswer(new Question("",null,null,null),new QuestionOption("")));
end

//decision rules
"""

class Question:
    rule_format = """
rule "Question {0}"
    when 
        QuestionAnswer(question.question == "{4}", answer.option == "{5}")
    then 
        insert(new Question("{0}",new QuestionOption("{1}"),new QuestionOption("{2}"),new QuestionOption("{3}")));
end  

"""
    rule_node = """
rule "Perfect typeface {0}"
    when 
        QuestionAnswer(question.question == "{4}", answer.option == "{5}")
    then 
        insert(new Question("Perfect typeface for you is {0}",null,null,null));
end  
            
    """

    question = ""
    answers = []
    prev_que = ""
    prev_ans = ""
    rule = ""

    def generate_rule(self):
        if self.answers[0] != "NODE":
            self.rule = self.rule_format.format(self.question, self.answers[0], self.answers[1],self.answers[2], self.prev_que,
                                                self.prev_ans)
        else:
            self.rule = self.rule_node.format(self.question, self.answers[0], self.answers[1], self.answers[2], self.prev_que,
                                              self.prev_ans)


datafile = sys.argv[1]
content = ""
with open(datafile) as f:
    content = [line.rstrip().split(';') for line in f.readlines()]
content = content[1:]

questions = []
for i in content:
    q = Question()
    q.answers = []

    q.question = i[0].replace("\"", "\\\"")
    j = 0
    for option in i[1].split(','):
        j += 1
        q.answers.append(option)
    for l in range(j, 3):
        q.answers.append("")

    q.prev_que = i[2]
    if '^' in q.prev_que:
        q.prev_que = questions[-len(q.prev_que)].question
    q.prev_ans = i[3]

    q.generate_rule()
    questions.append(q)

res = file_beginning
for q in questions:
    res += q.rule

print(res)
