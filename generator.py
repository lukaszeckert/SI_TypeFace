import sys

file_beginning = """
package com.sample
 
import javax.swing.*;

//declaring classes of object used in this project
declare Question
 	question : String 
	option1 : QuestionOption
	option2 : QuestionOption
end

declare QuestionOption
	option : String
end

declare QuestionAnswer
	question : Question
	answer : QuestionOption
end

//declaration of Gui helper functions

rule "Ask question0"
	when
		q: Question(option1 == null, option2 == null)
	then
		System.out.println(q.getQuestion());
		
		Object[] options = { "Ok","A","B"};
        JFrame frame = new JFrame("DialogDemo");
        frame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        int n = JOptionPane.showOptionDialog(null, q.getQuestion(), "",
                JOptionPane.YES_NO_OPTION, JOptionPane.QUESTION_MESSAGE,
                null, options, options[0]);
        insert( new QuestionAnswer(q,q.getOption1()));
end


rule "Ask question1"
	when
		q: Question(option1 != null, option2 == null)
	then
		System.out.println(q.getQuestion());
		
		Object[] options = { q.getOption1().getOption() };
        JFrame frame = new JFrame("DialogDemo");
        frame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        int n = JOptionPane.showOptionDialog(null, q.getQuestion(), "",
                JOptionPane.YES_NO_OPTION, JOptionPane.QUESTION_MESSAGE,
                null, options, options[0]);
        insert( new QuestionAnswer(q,q.getOption1()));
end


rule "Ask question2"
	when
		q: Question(option1 != null, option2 != null)
	then
		System.out.println(q.getQuestion());
		
		Object[] options = { q.getOption1().getOption(), q.getOption2().getOption()};
        JFrame frame = new JFrame("DialogDemo");
        frame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        int n = JOptionPane.showOptionDialog(null, q.getQuestion(), "",
                JOptionPane.YES_NO_OPTION, JOptionPane.QUESTION_MESSAGE,
                null, options, options[0]);
                
        insert( new QuestionAnswer(q,new QuestionOption((String)options[n])));
end

//decision rules
"""

class Question:
    rule_format = """
rule "Question {0}"
    when 
        QuestionAnswer(question.question == "{3}", answer.option == "{4}")
    then 
        insert(new Question("{0}",new QuestionOption("{1}"),new QuestionOption("{2}")));
end  

"""
    rule_node = """
rule "Perfect typeface {0}"
    when 
        QuestionAnswer(question.question == "{3}", answer.option == "{4}")
    then 
        insert(new Question("Perfect typeface for you is {0}",null,null));
end  
            
    """

    question = ""
    answers = []
    prev_que = ""
    prev_ans = ""
    rule = ""

    def generate_rule(self):
        if self.answers[0] != "NODE":
            self.rule = self.rule_format.format(self.question, self.answers[0], self.answers[1], self.prev_que,
                                                self.prev_ans)
        else:
            self.rule = self.rule_node.format(self.question, self.answers[0], self.answers[1], self.prev_que,
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
    for l in range(j, 2):
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
