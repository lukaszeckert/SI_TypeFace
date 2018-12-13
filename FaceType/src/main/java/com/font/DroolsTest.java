package com.font;

import javax.swing.JFrame;
import javax.swing.JButton;
import javax.swing.JLabel;
import javax.swing.SwingConstants;

import java.awt.FlowLayout;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;

import org.kie.api.KieServices;
import org.kie.api.runtime.KieContainer;
import org.kie.api.runtime.KieSession;




public class DroolsTest {

    public static final void main(String[] args) {
        try {
            // load up the knowledge base
	        KieServices ks = KieServices.Factory.get();
    	    KieContainer kContainer = ks.getKieClasspathContainer();
        	KieSession kSession = kContainer.newKieSession("ksession-rules");
        	HelloGui hg = new HelloGui(kSession);
        } catch (Throwable t) {
            t.printStackTrace();
        }
    }
}
class HelloGui extends JFrame implements ActionListener{
	JButton newFontJB;
	KieSession kSession;
	public HelloGui(KieSession kSession) {
		super("SO YOU NEED A TYPEFACE");
		
		this.kSession = kSession;
		
		setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
		setSize(450, 300);
		setLocation(50,50);
		setLayout(new FlowLayout());
		setResizable(false);
		String label = "<html><font color='green'>SO YOU NEED A TYPEFACE</font>"+
		"<br>is a project by Julian Hansen. It's an alternative way on how to"+
		"<br>choose fonts (or just be inspired) for a specific project, not just"+
		"<br>by browsing through the pages of FontBook. The list is (very loosely)"+
		"<br>based on the top 50 of Die 100 Besten Schriften by Font Shop"+
		"<br><br><br> Authors of implementation in Drools:"+
		"<br>Michal Dolata 132208"+
		"<br>Łukasz Eckert 132218"+
		"<br>Project for laboratory of Artificial Intelligence<br> on Poznan University of Technology"+
		"<br>Prowadzacy: dr inz. Artur Michalski </html>";
		JLabel jLabel = new JLabel(label);
		add(jLabel);
		newFontJB = new JButton("Find best font you!!!");
		newFontJB.setVerticalAlignment(SwingConstants.BOTTOM);
		add(newFontJB);
		newFontJB.addActionListener(this);
		setVisible(true);
	}

	@Override
	public void actionPerformed(ActionEvent arg0) {
		setVisible(false);
		kSession.fireAllRules();
		dispose();
		
	}
}
