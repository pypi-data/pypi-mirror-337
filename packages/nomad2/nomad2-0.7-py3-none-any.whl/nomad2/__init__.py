def slip1():
    print('''
//slip 1:
//Q.1:
public class prg extends
Thread
{
char c;
public void run()
{
for(c = 'A'; c<='Z';c++)
{
System.out.println(""+c);
try
{
Thread.sleep(3000);
}
catch(Exception e)
{
e.printStackTrace();
}
}
}
public static void main(String
args[])
{
prg t = new prg();
t.start();
}
}
//Q2.
import java.sql.*;
import java.awt.*;
import java.awt.event.*;
import javax.swing.*;
import java.util.*;


class emp extends JFrame implements ActionListener
{          
            JLabel l1,l2,l3,l4;
            JTextField t1,t2,t3;
            JButton b1,b2,b3;
            String sql;
            JPanel p,p1;
            Connection con;
            PreparedStatement ps;


            JTable t;
            JScrollPane js;
            ResultSet rs ;
            ResultSetMetaData rsmd ;
            int columns;
            Vector columnNames = new Vector();
            Vector data = new Vector();

            emp()
            {

                        l1 = new JLabel("Eno:");
                        l2 = new JLabel("Ename :");
                        l3 = new JLabel("Destination :");  
                        l4 = new JLabel("Salary :");        

                        t1 = new JTextField(20);
                        t2 = new JTextField(20);
                        t3 = new JTextField(20);

                        b1 = new JButton("Save");
                        b2 = new JButton("Display");
                        b3 = new JButton("Clear");

                        b1.addActionListener(this);
                        b2.addActionListener(this);
                        b3.addActionListener(this);

                        p=new JPanel();
                        p1=new JPanel();
                        p.add(l1);
                        p.add(t1);
                        p.add(l2);
                        p.add(t2);
                        p.add(l3);
                        p.add(t3);

                        p.add(b1);
                        p.add(b2);
                        p.add(b3);

                        add(p);
                        setLayout(new GridLayout(2,1));
                        setSize(600,800);
                        setVisible(true);
                        setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
            }
            public void actionPerformed(ActionEvent e)
            {
                        if((JButton)b1==e.getSource())
                        {
                                    int no = Integer.parseInt(t1.getText());
                                    String name = t2.getText();
                                    int p = Integer.parseInt(t3.getText());
                                    System.out.println("Accept Values");
                                    try
                                    {
                                                Class.forName( org.postgresql.Driver );
con=DriverManager.getConnection( jdbc:postgresql:ty","postgres","postgres );                                               

                                                
                                          int en=Integer.parseInt(t1.getText());
String enn=t2.getText();
int sal=Integer.parseInt(t3.getText());
String strr=”insert into emp values(” + en + ” ,'” + enn + “‘,” + sal
+ “)”;
int k=st.executeUpdate(strr);
if(k>0)
{
JOptionPane.showMessageDialog(null,”Record Is Added”);
}
}
catch(Exception er)
{
System.out.println(“Error”);
}
}
}
public static void main(String args[])
{
new emp().show();
}
}

''')
    

def slip2():
    print('''
//slip no.2
//Q1:
import java.util.*;
public class GFG {
public static void main(String args[])
{
// Creating a HashSet
HashSet<String> set = new HashSet<String>();
// Adding elements into HashSet using add()
set.add("geeks");
set.add("practice");
set.add("contribute");
set.add("ide");
System.out.println("Original HashSet: "
+ set);
List<String> list = new ArrayList<String>(set);
Collections.sort(list);
// Print the sorted elements of the HashSet
System.out.println("HashSet elements "+ "in sorted order "+ "using List: "+ list);
}
}
//Q2:
import java.io.*;
import javax.servlet.*;
import javax.servlet.http.*;
public class NewServlet extends HttpServlet
{
public void doGet(HttpServletRequest req,HttpServletResponse
resp)throws IOException,ServletException
{
resp.setContentType("text/html");
String userinfo=req.getHeader("User-Agent");
PrintWriter p=resp.getWriter();  
} 
}
<html>  
<body>
<form action="http://localhost:8080/serv/NewServlet"method="get">
Username:<input type="text" name="t1">
<input type="submit" >
</form>
</body>
</html>


''')
    

def slip3():
    print('''
//slip 3:
//Q1:
<!DOCTYPE html>

<html>

    <head>

        <meta http-equiv="Content-Type" content="text/html; charset=UTF-8">

        <title>JSP Page</title>

    </head>

    <body>

        <h1>Patient</h1>

        <table border="1">

            <tr>

                <th>PNo</th>

                <th>PName</th>

                <th>Address</th>

                <th>age</th>

                <th>disease</th>

            </tr>

            <tr>

                <td>1</td>

                <td>John</td>

                <td>xyz</td>

                <td>45</td>

                <td>kovid</td>

            </<tr>

            <tr>

                <td>2</td>

                <td>Brock</td>

                <td>abc</td>

                <td>48</td>

                <td>canser</td>

            </<tr>

        </table>

    </body>

</html>
//Q2:
import java.io.*;
// Java program to implement
// a Singly Linked List
public class LinkedList {
Node head; // head of list
// Linked list Node.
// Node is a static nested class
// so main() can access it
static class Node {
int data;
Node next;
// Constructor
Node(int d)
{
data = d;
next = null;
}
}
// Method to insert a new node
public static LinkedList insert(LinkedList
list,
int data)
{
// Create a new node with given data
Node new_node = new Node(data);
new_node.next = null;
// If the Linked List is empty,
// then make the new node as head
if (list.head == null) {
list.head = new_node;
}
else {
// Else traverse till the last node
// and insert the new_node there
Node last = list.head;
while (last.next != null) {
last = last.next;
}
// Insert the new_node at last
node
last.next = new_node;
}
// Return the list by head
return list;
}
public static void printList(LinkedList
list)
{
Node currNode = list.head;
System.out.print("LinkedList: ");
// Traverse through the LinkedList
while (currNode != null) {
// Print the data at current node
System.out.print(currNode.data +
" ");
// Go to next node
currNode = currNode.next;
}
System.out.println();
}
// **************DELETION BY
KEY**************
// Method to delete a node in the
LinkedList by KEY
public static LinkedList
deleteByKey(LinkedList list,
int
key)
{
// Store head node
Node currNode = list.head, prev =null;
// If head node itself holds the key to
be deleted
if (currNode != null &&
currNode.data == key) {
list.head = currNode.next; //
Changed head
// Display the message
System.out.println(key + " found
and deleted");
// Return the updated List
return list;
}
while (currNode != null &&
currNode.data != key) {
// If currNode does not hold key
// continue to next node
prev = currNode;
currNode = currNode.next;
}
if (currNode != null) {
// Since the key is at currNode
// Unlink currNode from linked
list
prev.next = currNode.next;
// Display the message
System.out.println(key + " found
and deleted");
}
if (currNode == null) {
System.out.println(key + " not
found");
}

return list;
}

public static void main(String[] args)
{
LinkedList list = new LinkedList();
list = insert(list, 1);
list = insert(list, 2);
list = insert(list, 3);
list = insert(list, 4);
list = insert(list, 5);
list = insert(list, 6);
list = insert(list, 7);
list = insert(list, 8);
// Print the LinkedList
printList(list);
deleteByKey(list, 1);
printList(list);
deleteByKey(list, 4);
printList(list);
deleteByKey(list, 10);
printList(list);
}
}



''')
    

def slip4():
    print('''
//slip 4:
//Q1:
import java.awt.*;
import java.awt.event.*;
class Slip8_1 extends Frame implements Runnable
{
Thread t;
Label l1;
int f;
Slip8_1()
{
t=new Thread(this);
t.start();
setLayout(null);
l1=new Label("Hello JAVA");
l1.setBounds(100,100,100,40);
add(l1);
setSize(300,300);
setVisible(true);
f=0;
}
public void run()
{
try
{
if(f==0)
{
t.sleep(200);
l1.setText("");
f=1;
}
if(f==1)
{
t.sleep(200);
l1.setText("Hello Java");
f=0;
}
}
catch(Exception e)
{
System.out.println(e);
}
run();
}
public static void main(String a[])
{
new Slip8_1();
}
}
//Q2:
import java.awt.*;
import java.awt.event.*;
import javax.swing.*;
import java.util.*;
class Slip16_2 extends JFrame implements ActionListener
{
JTextField t1,t2,t3;
JButton b1,b2,b3;
JTextArea t;
JPanel p1,p2;
Hashtable ts;
Slip16_2()
{
ts=new Hashtable();
t1=new JTextField(10);
t2=new JTextField(10);
t3=new JTextField(10);
b1=new JButton("Add");
b2=new JButton("Search");
b3=new JButton("Remove");
t=new JTextArea(20,20);
p1=new JPanel();
p1.add(t);
p2= new JPanel();
p2.setLayout(new GridLayout(2,3));
p2.add(t1);
p2.add(t2);
p2.add(b1);
p2.add(t3);
p2.add(b2);
p2.add(b3);
add(p1);
add(p2);
b1.addActionListener(this);
b2.addActionListener(this);
b3.addActionListener(this);
setLayout(new FlowLayout());
setSize(500,500);
setVisible(true);
setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
}
public void actionPerformed(ActionEvent e)
{
if(b1==e.getSource())
{
String name = t1.getText();
int code = Integer.parseInt(t2.getText());
ts.put(name,code);
Enumeration k=ts.keys();
Enumeration v=ts.elements();
String msg="";
while(k.hasMoreElements())
{
msg=msg+k.nextElement()+" = "+v.nextElement()+"\n";
}
t.setText(msg);
t1.setText("");
t2.setText("");
}
else if(b2==e.getSource())
{
String name = t3.getText();
if(ts.containsKey(name))
{
t.setText(ts.get(name).toString());
}
else
JOptionPane.showMessageDialog(null,"City not
found ...");
}
else if(b3==e.getSource())
{
String name = t3.getText();
if(ts.containsKey(name))
{
ts.remove(name);
JOptionPane.showMessageDialog(null,"City
Deleted ...");
}
else
JOptionPane.showMessageDialog(null,"City not
found ...");
}
}
public static void main(String a[])
{
new Slip16_2();
}
}

''')
    

def slip5():
    print('''
//slip no 5 
          //Q1

          import java.util.Enumeration;
import java.util.Hashtable;

public class StudentDetails {
    public static void main(String[] args) {

        // Create a HashTable to store mobile numbers and student names
        Hashtable<String, String> students = new Hashtable<>();

        // Add student details (Mobile Number → Name)
        students.put("9876543210", "Alice");
        students.put("9123456789", "Bob");
        students.put("9988776655", "Charlie");
        students.put("9556677889", "David");

        System.out.println("Student Details:");

        // Using Enumeration to iterate through the HashTable
        Enumeration<String> mobileNumbers = students.keys();

        while (mobileNumbers.hasMoreElements()) {
            String mobile = mobileNumbers.nextElement();
            String name = students.get(mobile);

            // Displaying the details
            System.out.println("Mobile: " + mobile + ", Name: " + name);
        }
    }
}

          
          //Q2

          <%@ page import="java.sql.*" %>
<html>
<head>
    <title>Online Quiz</title>
    <style>
        body { font-family: Arial, sans-serif; text-align: center; }
        .btn { padding: 10px 20px; margin: 10px; cursor: pointer; }
        .question { margin: 20px; }
    </style>
</head>
<body>

<%
    // Database connection parameters
    String dbUrl = "jdbc:mysql://localhost:3306/mcq_test";
    String dbUser = "root";
    String dbPass = "your_password";  // Replace with your MySQL password

    Connection conn = null;
    Statement stmt = null;
    ResultSet rs = null;

    // Check if the quiz has already been submitted
    boolean isSubmitted = request.getParameter("submit") != null;

    // Initialize score variable
    int score = 0;

    try {
        Class.forName("com.mysql.cj.jdbc.Driver");
        conn = DriverManager.getConnection(dbUrl, dbUser, dbPass);
        stmt = conn.createStatement();

        if (!isSubmitted) {
            // Display the quiz questions
            rs = stmt.executeQuery("SELECT * FROM questions ORDER BY RAND() LIMIT 3");
%>

<h1>Online Quiz</h1>

<form method="post" action="quiz.jsp">
    <%
        int i = 0;
        while (rs.next()) {
            i++;
    %>
    <div class="question">
        <p>Q<%= i %>: <%= rs.getString("question") %></p>
        <input type="radio" name="q<%= i %>" value="<%= rs.getString("option1") %>" required> <%= rs.getString("option1") %><br>
        <input type="radio" name="q<%= i %>" value="<%= rs.getString("option2") %>"> <%= rs.getString("option2") %><br>
        <input type="radio" name="q<%= i %>" value="<%= rs.getString("option3") %>"> <%= rs.getString("option3") %><br>
        <input type="radio" name="q<%= i %>" value="<%= rs.getString("option4") %>"> <%= rs.getString("option4") %>

        <!-- Store correct answer in hidden field -->
        <input type="hidden" name="a<%= i %>" value="<%= rs.getString("answer") %>">
    </div>
    <%
        }
    %>

    <input type="submit" name="submit" value="Submit" class="btn">
</form>

<%
        } else {
            // Calculate the score after submission
            for (int i = 1; i <= 3; i++) {
                String selected = request.getParameter("q" + i);
                String correct = request.getParameter("a" + i);

                if (selected != null && selected.equals(correct)) {
                    score++;
                }
            }
%>

<h1>Quiz Result</h1>
<h2>Your Score: <%= score %> / 3</h2>

<a href="quiz.jsp" class="btn">Try Again</a>

<%
        }
    } catch (Exception e) {
        e.printStackTrace();
    } finally {
        if (rs != null) rs.close();
        if (stmt != null) stmt.close();
        if (conn != null) conn.close();
    }
%>

</body>
</html>


''')
    

def slip6():
    print('''
//slip 6:
//Q1:
import java.util.*;
import java.io.*;
class Slip19_2
{
 public static void main(String[] args) throws Exception
 {
 int no,element,i;
 BufferedReader br=new BufferedReader(new
InputStreamReader(System.in));
 TreeSet ts=new TreeSet();
 System.out.println("Enter the of elements :");
 no=Integer.parseInt(br.readLine());
 for(i=0;i<no;i++)
 {
 System.out.println("Enter the element : ");
 element=Integer.parseInt(br.readLine());
 ts.add(element);
 }

 System.out.println("The elements in sorted order :"+ts);
 System.out.println("Enter element to be serach : ");
 element = Integer.parseInt(br.readLine());
 if(ts.contains(element))
 System.out.println("Element is found");
 else
 System.out.println("Element is NOT found");
 }
}
//Q2:
import java.applet.*;
import java.awt.*;
class Slip3_2 extends Applet implements Runnable
{
Thread t;
int r,g1,y,i;
public void init()
{
T=new Thread(this);
t.start();
r=0; g1=0;I=0; y=0;
}
public void run()
{
try
{
for(I =24; I >=1;i--)
{
if (I >16&& I <=24)
{
t.sleep(200);
r=1;
repaint();
}
if (I >8&& I <=16)
{
t.sleep(200);
y=1;
repaint();
}
if(I >1&& I <=8)
{
t.sleep(200);
g1=1;
repaint();
}
}
if (I ==0)
{
run();
}
}
catch(Exception e)
{ System.out.println(e);
}
} public void paint(Graphics g)
{
g.drawRect(100,100,100,300);
if (r==1)
{
g.setColor(Color.red);
g.fillOval(100,100,100,100);
g.setColor(Color.black);
g.drawOval(100,200,100,100);
g.drawOval(100,300,100,100);
r=0;
}
if (y==1)
{
g.setColor(Color.black);
g.drawOval(100,100,100,100);
g.drawOval(100,300,100,100);
g.setColor(Color.yellow);
g.fillOval(100,200,100,100);
y=0;
}
if (g1==1)
{
g.setColor(Color.black);
g.drawOval(100,100,100,100);
g.drawOval(100,200,100,100);
g.setColor(Color.green);
g.fillOval(100,300,100,100);
g1=0;
}
}
} 

''')
    

def slip7():
    print('''
//slip 7:
//Q1:
import java.util.Random;
class Square extends Thread
{
 int x;
 Square(int n)
 {
 x = n;
 }
 public void run()
 {
 int sqr = x * x;
 System.out.println("Square of " + x + " =
" + sqr );
 }
}
class Cube extends Thread
{
 int x;
 Cube(int n)
 {x = n;
 }
 public void run()
 {
 int cub = x * x * x;
 System.out.println("Cube of " + x + " = "
+ cub );
 }
}
class Number extends Thread
{
 public void run()
 {
 Random random = new Random();
 for(int i =0; i<5; i++)
 {
 int randomInteger = random.nextInt(100);
 System.out.println("Random Integer
generated : " + randomInteger);
 Square s = new Square(randomInteger);
 s.start();
 Cube c = new Cube(randomInteger);
 c.start();
 try {
 Thread.sleep(1000);
} catch (InterruptedException ex) {
 System.out.println(ex);
}
}
 }
}
public class Thr {
 public static void main(String args[])
 {
 Number n = new Number();
 n.start();
 }
}
//Q2:
/Create table student with fields roll number,name,percentage using postgresql. Insert values in the tables. Display all the details of the student table in the tabular format on the screen(using swing)./

import java.sql.*;
import java.awt.*;
import java.awt.event.*;
import javax.swing.*;
import java.util.*;


class product extends JFrame implements ActionListener
{          
            JLabel l1,l2,l3;
            JTextField t1,t2,t3;
            JButton b1,b2,b3;
            String sql;
            JPanel p,p1;
            Connection con;
            PreparedStatement ps;


            JTable t;
            JScrollPane js;
            Statement stmt ;
            ResultSet rs ;
            ResultSetMetaData rsmd ;
            int columns;
            Vector columnNames = new Vector();
            Vector data = new Vector();

            product()
            {

                        l1 = new JLabel("Enter pid:");
                        l2 = new JLabel("Enter pname :");
                        l3 = new JLabel("price :");       

                        t1 = new JTextField(20);
                        t2 = new JTextField(20);
                        t3 = new JTextField(20);

                        b1 = new JButton("Save");
                        b2 = new JButton("Display");
                        b3 = new JButton("Clear");

                        b1.addActionListener(this);
                        b2.addActionListener(this);
                        b3.addActionListener(this);

                        p=new JPanel();
                        p1=new JPanel();
                        p.add(l1);
                        p.add(t1);
                        p.add(l2);
                        p.add(t2);
                        p.add(l3);
                        p.add(t3);

                        p.add(b1);
                        p.add(b2);
                        p.add(b3);

                        add(p);
                        setLayout(new GridLayout(2,1));
                        setSize(600,800);
                        setVisible(true);
                        setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
            }
            public void actionPerformed(ActionEvent e)
            {
                        if((JButton)b1==e.getSource())
                        {
                                    int no = Integer.parseInt(t1.getText());
                                    String name = t2.getText();
                                    int p = Integer.parseInt(t3.getText());
                                    System.out.println("Accept Values");
                                    try
                                    {
                                                Class.forName( org.postgresql.Driver );
con=DriverManager.getConnection( jdbc:postgresql:ty","postgres","postgres );                                               
sql = "insert into product values(?,?,?)";
                                                ps = con.prepareStatement(sql);
                                                ps.setInt(1,pid);
                                                ps.setString(2, pname);
                                                ps.setInt(3,price);
                                                System.out.println("values set");
                                                int n=ps.executeUpdate();
                                                if(n!=0)
                                                {
                                                            JOptionPane.showMessageDialog(null,"Record insered ...");                                  
                                                }

                                                else
                                                            JOptionPane.showMessageDialog(null,"Record NOT inserted ");

                                    }//end of try
                                    catch(Exception ex)
                                    {
                                                System.out.println(ex);          
                                                //ex.printStackTrace();
                                    }

                        }//end of if
                        else if((JButton)b2==e.getSource())
                        {
                                    try
                                    {
                                                Class.forName( org.postgresql.Driver );
con=DriverManager.getConnection( jdbc:postgresql://192.168.100.254/Bill , oracle , oracle );
                                                System.out.println("Connected");
                                                stmt=con.createStatement();
                                                rs = stmt.executeQuery("select * from product");
                                                rsmd = rs.getMetaData();
                                                columns = rsmd.getColumnCount();

                                                //Get Columns name
                                                for(int i = 1; i <= columns; i++)
                                                {
                                                            columnNames.addElement(rsmd.getColumnName(i));
                                                }

                                                //Get row data
                                                while(rs.next())
                                                {
                                                            Vector row = new Vector(columns);
                                                            for(int i = 1; i <= columns; i++)
                                                            {
                                                                        row.addElement(rs.getObject(i));
                                                            }
                                                            data.addElement(row);
                                                }
                                                t = new JTable(data, columnNames);
                                                js = new JScrollPane(t);

                                                p1.add(js);
                                                add(p1);

                                                setSize(600, 600);
                                                setVisible(true);
                                    }
                                    catch(Exception e1)
                                    {
                                                System.out.println(e1);
                                    }
                        }
                        else
                        {
                                    t1.setText(" ");
                                    t2.setText(" ");
                                    t3.setText(" ");

                        }
            }//end of method

            public static void main(String a[])
            {
                        product ob = new product();
            }
}


''')
    

def def8():
    print('''
//slip 8
//Q1:
public class A1 extends Thread {
 String str;
 int n;
 A1(String str, int n) {
 this.str = str;
 this.n = n;
 }

 public void run() {
 try {
 for (int i = 0; i < n; i++) {

System.out.println(getName() + " : " +
str);
 }
 } catch (Exception e) {
 e.printStackTrace();
 }
 }
 public static void main(String[] args)
{
 A1 t1 = new A1("COVID19", 10);
 A1 t2 = new A1("LOCKDOWN2020", 20);
 A1 t3 = new A1("VACCINATED", 30);
t1.start();
 t2.start();
 t3.start();
 }
}
//Q2:
<html>
 <head>
 <meta http-equiv="Content-Type" content="text/html;
charset=UTF-8">
 <title>JSP Page</title>
 </head>
 <body><center><h1>The required Result is:: </h1>
 <h2>
 <%
 int n,i,flag=0;
 String ns= request.getParameter("n");
 n=Integer.parseInt(ns);
 if(n>1)
 {
 for(i=2;i<=n/2;i++)
 {
 if(n%i==0)
 {
 flag=1;
break;
 }
 }
 }
 if(flag==0)
 {
 out.println("<pre>");
 out.println(n+" is a prime no.");
 out.println("</pre>");
 }
 else
 {
 out.println("<pre>");
 out.println(n+" is not a prime no.");
 out.println("</pre>");
 }
 %>
 </h2></center>
 </body>
</html>




''')
    

def slip9():
    print('''
//slip 9:
//Q1:
import java.awt.*;import java.awt.geom.*;import javax.swing.*;import java.awt.event.*;import
java.util.*;
public class BouncingBallApp extends JFrame
{
 //start of main method
 public static void main(String[] args)
 {
 //crate container
 Container container = new Container();
 //crate BouncingBallApp instance
 BouncingBallApp bBalls = new BouncingBallApp();
 //set the window closing feature(close with X click)
 bBalls.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
 //crate boucing ball panel(BBP) instance and add
 BouncingBallPanel BBP = new BouncingBallPanel();
 container.add(BBP);
 //make the BBP the MouseListner
 bBalls.addMouseListener(BBP);
 //set window background and size
 bBalls.setBackground(Color.WHITE);
 bBalls.setSize(400, 300);
 BBP.setSize(400, 300);
 BBP.setLayout(null);
 bBalls.setContentPane(BBP);
 //set window visible
 bBalls.setVisible(true);
 }
}
class BouncingBallPanel extends JPanel implements MouseListener
{
 //create an empty array for 20 Ball objects
 public Ball[] array;
 private int count = 0;
 Random generator = new Random();
public BouncingBallPanel()
 {
 array = new Ball[20];
 }
 public void mouseClicked(MouseEvent event)
 {
 array[count] = new Ball(this);
 count++;
 if( count == 1)
 {
 final Runnable update = new Runnable()
 {
 public void run()
 {
 for (int j = 0; j < array.length; j++)
 {
 if(array[j] != null)
 {
 array[j].move();
 }//end of if
 }//end of for
 }//end of run method
 };//end of runnalbe update
 (new Thread(new Ball(this))).start();
 Runnable graphic = new Runnable()
 {
 public void run()
 {
 while(true)
 {
 try
 {
 EventQueue.invokeLater(update);
 Thread.sleep(generator.nextInt(10 +100));
 }catch (InterruptedException exp){}
 }//end of while
 }//end of run
 };//end of runnable
 new Thread(graphic).start();
 }//end of if
 }//end of mouseClicked method
 //empty interfaces for mouse events
 public void mouseExited(MouseEvent event){}
 public void mouseReleased(MouseEvent event){}
 public void mouseEntered(MouseEvent event){}
 public void mousePressed(MouseEvent event){}
 //paint component method
 public void paintComponent(Graphics g)
 {
 super.paintComponent(g);
 Graphics2D g2d = (Graphics2D) g;
 //loop for each ball and draw all balls in array
 for(int i = 0; i < array.length; i++)
 {
 if(array[i] != null)
 {
 g2d.setColor(array[i].getColor());
g2d.fillOval((int)array[i].getX(), (int)array[i].getY(), (int)array[i].getDiameter(),
(int)array[i].getDiameter());
 }
 }//end of for loop
 }//end of paintComponent loop
}//end of Class BouncingBallPanel
class Ball implements Runnable
{
 //set up variables
 private double x;
 private double y;
 private int deltaX;
 private int deltaY;
 private double diameter;
 private Color color;
 BouncingBallPanel BBP2;
 Random random = new Random();
 public Ball(BouncingBallPanel a)
 {
 x = random.nextInt(400);
 y = random.nextInt(300);
 deltaX = 1 + random.nextInt(10);
 deltaY = 1 + random.nextInt(10);
 diameter = 5 + random.nextInt(20);
 color = new Color(random.nextInt(256), random.nextInt(256), random.nextInt(256));
 BBP2 = a;
 }// end of constructor
 public double getX()
 {
 return x;
 }
 public double getY() {
 return y;
 }
 public double getDiameter() {
 return diameter;
 }
 public Color getColor() {
 return color;
 }
 public void move() {
 x += deltaX;
 y += deltaY;
 if (x > 400 - getDiameter()|| x <0)
 {
 deltaX = -deltaX;
 }
 if (y > 300 - getDiameter() || y < 0)
 {
 deltaY = -deltaY;
 }
}// end of method move
 @Override
 public void run()
 {
 while(true)
 {
 move();
 BBP2.repaint();
 try{
 Thread.currentThread().sleep(10 + random.nextInt(100));
 }catch(InterruptedException exp){}
 }//end of while
 }//end of run method
}
//Q2:
import java.util.*;
import java.io.*;
class Slip19_2
{
 public static void main(String[] args) throws Exception
 {
 int no,element,i;
 BufferedReader br=new BufferedReader(new
InputStreamReader(System.in));
 TreeSet ts=new TreeSet();
 System.out.println("Enter the of elements :");
 no=Integer.parseInt(br.readLine());
 for(i=0;i<no;i++)
 {
 System.out.println("Enter the element : ");
 element=Integer.parseInt(br.readLine());
 ts.add(element);
 }

 System.out.println("The elements in sorted order :"+ts);
 System.out.println("Enter element to be serach : ");
 element = Integer.parseInt(br.readLine());
 if(ts.contains(element))
 System.out.println("Element is found");
 else
 System.out.println("Element is NOT found");
 }
}




''')
    

def slip10():
    print('''
//slip 10
//Q1:
import java.text.*;
import java.util.*;
public class GFG {
public static void main(String args[])
{
SimpleDateFormat formatDate = new
SimpleDateFormat(
"dd/MM/yyyy HH:mm:ss z");
//"SimpleDateFormat" class
initialize with object
//"formatDate" this class acceptes
the format of
// date and time as ""dd/MM/yyyy"
and "HH:mm:ss z""
//"z" use for print the time zone
Date date = new Date();
// initialize "Date" class
formatDate.setTimeZone(TimeZone.getTimeZone
("IST"));
// converting to IST or format the
Date as IST
System.out.println(formatDate.format(date))
;
// print formatted date and time
}
}
//Q2:
/Create table student with fields roll number,name,percentage using postgresql. Insert values in the tables. Display all the details of the student table in the tabular format on the screen(using swing)./

import java.sql.*;
import java.awt.*;
import java.awt.event.*;
import javax.swing.*;
import java.util.*;


class stud_info extends JFrame implements ActionListener
{          
            JLabel l1,l2,l3;
            JTextField t1,t2,t3;
            JButton b1,b2,b3;
            String sql;
            JPanel p,p1;
            Connection con;
            PreparedStatement ps;


            JTable t;
            JScrollPane js;
            Statement stmt ;
            ResultSet rs ;
            ResultSetMetaData rsmd ;
            int columns;
            Vector columnNames = new Vector();
            Vector data = new Vector();

            stud_info()
            {

                        l1 = new JLabel("Enter no :");
                        l2 = new JLabel("Enter name :");
                        l3 = new JLabel("percentage :");       

                        t1 = new JTextField(20);
                        t2 = new JTextField(20);
                        t3 = new JTextField(20);

                        b1 = new JButton("Save");
                        b2 = new JButton("Display");
                        b3 = new JButton("Clear");

                        b1.addActionListener(this);
                        b2.addActionListener(this);
                        b3.addActionListener(this);

                        p=new JPanel();
                        p1=new JPanel();
                        p.add(l1);
                        p.add(t1);
                        p.add(l2);
                        p.add(t2);
                        p.add(l3);
                        p.add(t3);

                        p.add(b1);
                        p.add(b2);
                        p.add(b3);

                        add(p);
                        setLayout(new GridLayout(2,1));
                        setSize(600,800);
                        setVisible(true);
                        setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
            }
            public void actionPerformed(ActionEvent e)
            {
                        if((JButton)b1==e.getSource())
                        {
                                    int no = Integer.parseInt(t1.getText());
                                    String name = t2.getText();
                                    int p = Integer.parseInt(t3.getText());
                                    System.out.println("Accept Values");
                                    try
                                    {
                                                Class.forName( org.postgresql.Driver );
con=DriverManager.getConnection( jdbc:postgresql:ty","postgres","postgres );                                               
sql = "insert into stud values(?,?,?)";
                                                ps = con.prepareStatement(sql);
                                                ps.setInt(1,no);
                                                ps.setString(2, name);
                                                ps.setInt(3,p);
                                                System.out.println("values set");
                                                int n=ps.executeUpdate();
                                                if(n!=0)
                                                {
                                                            JOptionPane.showMessageDialog(null,"Record insered ...");                                  
                                                }

                                                else
                                                            JOptionPane.showMessageDialog(null,"Record NOT inserted ");

                                    }//end of try
                                    catch(Exception ex)
                                    {
                                                System.out.println(ex);          
                                                //ex.printStackTrace();
                                    }

                        }//end of if
                        else if((JButton)b2==e.getSource())
                        {
                                    try
                                    {
                                                Class.forName( org.postgresql.Driver );
con=DriverManager.getConnection( jdbc:postgresql://192.168.100.254/Bill , oracle , oracle );
                                                System.out.println("Connected");
                                                stmt=con.createStatement();
                                                rs = stmt.executeQuery("select * from stud");
                                                rsmd = rs.getMetaData();
                                                columns = rsmd.getColumnCount();

                                                //Get Columns name
                                                for(int i = 1; i <= columns; i++)
                                                {
                                                            columnNames.addElement(rsmd.getColumnName(i));
                                                }

                                                //Get row data
                                                while(rs.next())
                                                {
                                                            Vector row = new Vector(columns);
                                                            for(int i = 1; i <= columns; i++)
                                                            {
                                                                        row.addElement(rs.getObject(i));
                                                            }
                                                            data.addElement(row);
                                                }
                                                t = new JTable(data, columnNames);
                                                js = new JScrollPane(t);

                                                p1.add(js);
                                                add(p1);

                                                setSize(600, 600);
                                                setVisible(true);
                                    }
                                    catch(Exception e1)
                                    {
                                                System.out.println(e1);
                                    }
                        }
                        else
                        {
                                    t1.setText(" ");
                                    t2.setText(" ");
                                    t3.setText(" ");

                        }
            }//end of method

            public static void main(String a[])
            {
                        stud_info ob = new stud_info();
            }
}


''')
    

def slip11():
    print('''
//slip 11:
//Q1:
import java.io.*;
import javax.servlet.*;
import javax.servlet.http.*;
import java.sql.*;
public class servletDatabase extends HttpServlet
{ 
Connection cn;
public void init()
{
try
{
Class.forName("org.gjt.mm.mysql.Driver");
cn=DriverManager.getConnection("jdbc:mysql://
localhost/stud","root","password");
System.out.println("Hii");
}
catch(Exception ce)
{  
System.out.println("Error"+ce.getMessage());
}
}
public void doGet(HttpServletRequest req, HttpServletResponse
resp)
throws ServletException, IOException
{
resp.setContentType("text/html");
PrintWriter pw=resp.getWriter();  
try
{
int
rno=Integer.parseInt(req.getParameter("t1"));  
String qry="Select * from student where
rollno="+rno;  
Statement st=cn.createStatement();
ResultSet rs=st.executeQuery(qry);  
while(rs.next())
{
pw.print("<table border=1>");
pw.print("<tr>");
pw.print("<td>" + rs.getInt(1) + "</td>");
pw.print("<td>" + rs.getString(2) + "</td>");
pw.print("<td>" + rs.getFloat(3) + "</td>");
pw.print("</tr>");
pw.print("</table>");
}
}
catch(Exception se){}
pw.close();
}
}
HTML File
<html>
<body>
<form
action="http://localhost:8080/servDb/servletDatabase"
method="get">
Enter Roll No:<input type="text" name="t1">
<input type="submit">
</form>
</body>
</html>
pssql> create database stud;
Query OK, 1 row affected (0.00 sec)
pssql> create table student(rollno int primary key,name
text,percentage float);
Query OK, 0 rows affected (0.07 sec)
pssql> insert into student values(1,'student1',79);
Query OK, 1 row affected (0.04 sec)
pssql> insert into student values(2,'student2',69);
Query OK, 1 row affected (0.05 sec)
pssql> insert into student values(3,'student3',58);
Query OK, 1 row affected (0.06 sec)
pssql> select * from student;
//Q2:
/*-- create table donor(did int, dname char(22),daddr varchar(22));

-- insert into donor VALUES(1,'AAA','zzz');
-- insert into donor VALUES(2,'BBB','yyy');
-- insert into donor VALUES(3,'CCC','xxx');
-- insert into donor VALUES(4,'DDD','www');

SELECT * from donor;    */

/*
Write a program to display information about all coumns in the DONOR table using ResultSetMetaData.
 */

import java.sql.*;

public class DONOR {
    public static void main(String[] args) 
{
        try 
        {
            // load a driver
            Class.forName("org.postgresql.Driver");

            // Establish Connection
            Connection conn = DriverManager.getConnection("jdbc:postgresql://localhost/postgres", "postgres", "dsk");

            Statement stmt = null;
            stmt = conn.createStatement();
            ResultSet rs = stmt.executeQuery("select * from donor");

            ResultSetMetaData rsmd = rs.getMetaData();
            System.out.println("\t-------------------------------------------------");

            int count = rsmd.getColumnCount();
            System.out.println("\t No. of Columns: " + rsmd.getColumnCount());
            System.out.println("\t-------------------------------------------------");
            for (int i = 1; i <= count; i++) 
            {
                System.out.println("\t\tColumn No : " + i);
                System.out.println("\t\tColumn Name : " + rsmd.getColumnName(i));
                System.out.println("\t\tColumn Type : " + rsmd.getColumnTypeName(i));
                System.out.println("\t\tColumn Display Size : " + rsmd.getColumnDisplaySize(i));
                System.out.println();
            } // for
            System.out.println("\t--------------------------------------------------");

            rs.close();
            stmt.close();
            conn.close();
        } // try
            catch (Exception e) 
            {
                        System.out.println(e);
            } // catch
    }
}






''')
    

def slip12():
    print('''
//slip 12:
//Q1:
Index.html file:
<!DOCTYPE html>
<html>
<head>
<title>PERFECT NUMBER</title>
</head>
<body>
<form action="perfect.jsp" method="post">
Enter Number :<input type="text" name="num">
<input type="submit" value="Submit" name="s1">
</form>
</body>
</html>
Perfect.jsp file:
<%@ page import="java.util.*" %>
<%
if(request.getParameter("s1")!=null)
 {
Integer num,a,i,sum = 0;
num = Integer.parseInt(request.getParameter("num"));
a = num;
for(i=1;i<a;i++)
{
if(a%i==0)
{
sum=sum + i;
}
}
if(sum==a)
{
out.println(+num+ "is a perfect number");
}
else
{
out.println(+num+ "is not a perfect number");
}
 }
%>
//Q2:
package pro details;
import java.awt.*
import java.sql.*;
import javax.swing.*;
import javax.swing.table.DefaultTableModel:
public class Pro details
public static void main(String[] args)
SwingUtilities. InvokeLater(new Runnable()
public void run()
{
new Pro_details().createAndShowGJI();
});
public void createAndShowGUI()
{
JFrame frame new = new JFrame("Project table Details"); 
frame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);

frame.setSize(600,400);

JTable table= new JTable();

JScrollPane scrollPane =new JScrollPane(table); 
frame.add(scrollPane, BorderLayout.CENTER);

LoadData(table);

frame.setVisible(true);
}
private void loadData(JTable table)
String url="jdbc:postgresql:postgres";
String password="redhat"; 
String username="postgres";
Connection conn=null;

Statement stet= null;

ResultSet rs=null;

try
{
conn= DriverManager.getConnection(url, username.password);
 String query ="SELECT FROM project";

stat=conn.createStatement();
rs=stmt.executeQuery(query);

ResultSetMetaData metaData=rs.getMetaData();
int columnCount=metaData.getColumnCount();

String[] columnNames=new String[columnCount];

for (int=0;1<columnCount; i++)
{
columnNames [i]=metaData.getColumnName (i+1);
}
DefaultTableModel model=new DefaultTaableModel(columnNames,0);
while(rs.next())
{
Object[] rowData=new Object[columnCount];

for(int i=0;i<columnCount; i++)
{
  rowData[i]=rs.getObject(i+1);
} 
model.addRow(rowData);
}
table.setModel(model);
}
catch(SQLException e)
{
e.printStackTrace();

JOptionPane.showMessageDialog(null, "Error connecting to the database .", "Error", JOptionPane. ERROR MESSAGE);
}
finally
{
try
{

if (rs!=null) rs.close();

if(stat!=null)stmt.close();

if (conn!=null)conn.close();
}
catch(SQLException e)
{
e.printStackTrace();
}
}
}
}




''')
    

def slip13():
    print('''
//slip 13:
//Q1:
import java.sql.*;
import java.io.*;
public class DBMetaData
{
public static void main(String[] args) throws Exception
{
ResultSet rs = null;
Class.forName("org.postgresql.Driver");
Connection conn =DriverManager.getConnection("jdbc:postgresql://localhost/dbtry","postgres","redhat");
DatabaseMetaData dbmd = conn.getMetaData();
System.out.println("Database Product name = " +
dbmd.getDatabaseProductName());
System.out.println("User name = " + dbmd.getUserName());
System.out.println("Database driver name= " +
dbmd.getDriverName());
System.out.println("Database driver version = "+
dbmd.getDriverVersion());
System.out.println("Database product name = " +
dbmd.getDatabaseProductName());
System.out.println("Database Version = " +
dbmd.getDriverMajorVersion());
rs = dbmd.getTables(null,null,null, new String[]{"TABLE"});
System.out.println("List of tables...");
while(rs.next())
{
String tblName = rs.getString("TABLE_NAME");
System.out.println("Table : "+ tblName);
}
conn.close();
}
}
//Q2:
Class MyThread extends Thread
{ public MyThread(String s)
{
super(s);
}
public void run()
{
System.out.println(getName()+"thread created.");
while(true)
{
System.out.println(this);
int s=(int)(math.random()*5000);
System.out.println(getName()+"is sleeping for :+s+"msec");
try{
Thread.sleep(s);
}
catch(Exception e)
{
}
}
}
Class ThreadLifeCycle
{
public static void main(String args[])
{
MyThread t1=new MyThread("shradha"),t2=new MyThread("pooja");
t1.start();
t2.start();
try
{
t1.join();
t2.join();
}
catch(Exception e)
{
}
System.out.println(t1.getName()+"thread dead.");
System.out.println(t2.getName()+"thread dead.");
}
}

''')
    

def slip14():
    print('''
//slip 14:
//Q1:
import java.io.*;
public class SearchThread extends Thread
{
File f1;
String fname;
static String str;
String line;
LineNumberReader reader = null;
SearchThread(String fname)
{
this.fname=fname;
f1=new File(fname);
}
public void run()
{  
try
{
FileReader fr=new FileReader(f1);
reader=new LineNumberReader(fr);
while((line=reader.readLine())!=null)
{
if(line.indexOf(str)!=-1)
{
System.out.println("string found in
"+fname+"at "+reader.getLineNumber()+"line");
stop();
}
}
}
catch(Exception e)
{
}
}  
public static void main(String[] args) throws IOException
{
Thread t[]=new Thread[20];
BufferedReader br=new BufferedReader(new
InputStreamReader(System.in));
System.out.println("Enter String to search");
str=br.readLine();
FilenameFilter filter = new FilenameFilter()
{
public boolean accept(File file, String name)
{
if (name.endsWith(".txt"))
{
return true;
}
else
{
return false;
}
}
};
File dir1 = new File(".");
File[] files = dir1.listFiles(filter);
if (files.length == 0)
{
System.out.println("no files available with this
extension");
}
else
{
for(int i=0;i<files.length;i++)
{
for (File aFile : files)
{
t[i]=new SearchThread(aFile.getName());
t[i].start();
}
}
}
}
}
//Q2:
HTML FILE
<!DOCTYPE html>
<html>
<body>
<form method=post action="Slip7.jsp">
Enter Any Number : <Input type=text name=num><br><br>
<input type=submit value=Display>
</form>
</body>
</html>
JSP FILE:
<%@page contentType="text/html" pageEncoding="UTF-8"%>
<!DOCTYPE html>
<html>
<body>
<%! int n,rem,r; %>
<% n=Integer.parseInt(request.getParameter("num"));
if(n<10)
{
out.println("Sum of first and last digit is ");
%><font size=18 color=red><%= n %></font>
<%
}
else
{
rem=n%10;
do{
r=n%10;
n=n/10;
}while(n>0);
n=rem+r;
out.println("Sum of first and last digit is ");
%><font size=18 color=red><%= n %></font>
<%
}
%>
</body>
</html>

''')
    

def slip15():
    print('''
//slip 15:
//Q1:
public class MainThread
{
 public static void main(String arg[])
 {
 Thread t=Thread.currentThread();
 System.out.println("Current Thread:"+t);//Change Name
t.setName("My Thread ");
 System.out.println ("After the name is Changed:"+t);
 try {
 for(int i=2;i>0;i--)
 {
 System.out.println(i);
 Thread.sleep(1000);
 }
 }
catch(Exception e)
 {
 System.out.println(e);
 }
 }
}
//Q2:
import java.io.*;
 import javax.servlet.*;
 import javax.servlet.http.*;public class VisitServlet extends
HttpServlet
{
 static int i=1;
 public void doGet(HttpServletRequest request,HttpServletResponse
response)
throws IOException,ServletException
 {
 response.setContentType("text/html");
 PrintWriter out=response.getWriter();
 String k=String.valueOf(i);
 Cookie c=new Cookie("visit",k);
 response.addCookie(c);
 int j=Integer.parseInt(c.getValue());
 if(j==1)
 {
 out.println("Welcome to web page ");
 }
 else {
 out.println("You are visited at "+i+" times");
 }
 i++;
}
}
Web.xml
<?xml version="1.0" encoding="ISO-8859-1"?>
<web-app>
<servlet>
<servlet-name>VisitServlet</servlet-name>
<servlet-class>VisitServlet</servlet-class>
</servlet>
 36<servlet-mapping>
<servlet-name>VisitServlet</servlet-name>
<url-pattern>/VS</url-pattern>
</servlet-mapping>
</web-app>

''')
    
def slip16():
    print('''
//slip no 16
//Q1:
 import java.util.Scanner;
import java.util.TreeSet;
public class a2
{
public static void main(String args[])
{
Scanner sc=new Scanner(System.in);
TreeSet<Object> ts= new TreeSet<>();
System.out.println("Enter how many Colours");
int n=sc.nextInt();
System.out.println("Enter the "+n+"Colours:");
for(int i=0;i<n;i++)
{
String c=sc.next();
ts.add(c);
}
System.out.println("Colours:"+ts);
sc.close();
}
}
//Q2:

import java.sql.*;
import java.awt.*;
import java.awt.event.*;
import javax.swing.*;
import java.util.*;


class teacher extends JFrame implements ActionListener
{          
            JLabel l1,l2,l3;
            JTextField t1,t2,t3;
            JButton b1,b2,b3;
            String sql;
            JPanel p,p1;
            Connection con;
            PreparedStatement ps;


            JTable t;
            JScrollPane js;
            Statement stmt ;
            ResultSet rs ;
            ResultSetMetaData rsmd ;
            int columns;
            Vector columnNames = new Vector();
            Vector data = new Vector();

            teacher()
            {

                        l1 = new JLabel("no :");
                        l2 = new JLabel("Tname :");
                        l3 = new JLabel("subject :");       

                        t1 = new JTextField(20);
                        t2 = new JTextField(20);
                        t3 = new JTextField(20);

                        b1 = new JButton("Save");
                        b2 = new JButton("Display");
                        b3 = new JButton("Clear");

                        b1.addActionListener(this);
                        b2.addActionListener(this);
                        b3.addActionListener(this);

                        p=new JPanel();
                        p1=new JPanel();
                        p.add(l1);
                        p.add(t1);
                        p.add(l2);
                        p.add(t2);
                        p.add(l3);
                        p.add(t3);

                        p.add(b1);
                        p.add(b2);
                        p.add(b3);

                        add(p);
                        setLayout(new GridLayout(2,1));
                        setSize(600,800);
                        setVisible(true);
                        setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
            }
            public void actionPerformed(ActionEvent e)
            {
                        if((JButton)b1==e.getSource())
                        {
                                    int no = Integer.parseInt(t1.getText());
                                    String name = t2.getText();
                                    int p = Integer.parseInt(t3.getText());
                                    System.out.println("Accept Values");
                                    try
                                    {
                                                Class.forName( org.postgresql.Driver );
con=DriverManager.getConnection( jdbc:postgresql:ty","postgres","postgres );                                               
sql = "insert into teacher values(?,?,?)";
                                                ps = con.prepareStatement(sql);
                                                ps.setInt(1,no);
                                                ps.setString(2, name);
                                                ps.setInt(3,p);
                                                System.out.println("values set");
                                                int n=ps.executeUpdate();
                                                if(n!=0)
                                                {
                                                            JOptionPane.showMessageDialog(null,"Record insered ...");                                  
                                                }

                                                else
                                                            JOptionPane.showMessageDialog(null,"Record NOT inserted ");

                                    }//end of try
                                    catch(Exception ex)
                                    {
                                                System.out.println(ex);          
                                                //ex.printStackTrace();
                                    }

                        }//end of if
                        else if((JButton)b2==e.getSource())
                        {
                                    try
                                    {
                                                Class.forName( org.postgresql.Driver );
con=DriverManager.getConnection( jdbc:postgresql://192.168.100.254/Bill , oracle , oracle );
                                                System.out.println("Connected");
                                                stmt=con.createStatement();
                                                rs = stmt.executeQuery("select * from stud");
                                                rsmd = rs.getMetaData();
                                                columns = rsmd.getColumnCount();

                                                //Get Columns name
                                                for(int i = 1; i <= columns; i++)
                                                {
                                                            columnNames.addElement(rsmd.getColumnName(i));
                                                }

                                                //Get row data
                                                while(rs.next())
                                                {
                                                            Vector row = new Vector(columns);
                                                            for(int i = 1; i <= columns; i++)
                                                            {
                                                                        row.addElement(rs.getObject(i));
                                                            }
                                                            data.addElement(row);
                                                }
                                                t = new JTable(data, columnNames);
                                                js = new JScrollPane(t);

                                                p1.add(js);
                                                add(p1);

                                                setSize(600, 600);
                                                setVisible(true);
                                    }
                                    catch(Exception e1)
                                    {
                                                System.out.println(e1);
                                    }
                        }
                        else
                        {
                                    t1.setText(" ");
                                    t2.setText(" ");
                                    t3.setText(" ");

                        }
            }
private void select(Connection conn) throws SQLException {

        String sql = "select * from teacher where subject = 'java'";

       

        Statement stmt = conn.createStatement();

       

        ResultSet rs = stmt.executeQuery(sql);

        while(rs.next()) {

            System.out.println("teacher tno: " + rs.getInt("tno"));

            System.out.println("teacher tname: " + rs.getString("tname"));

            System.out.println("teacher subject: " + rs.getString("subject"));

        }

    }

}

            public static void main(String a[])
            {
                        teacher ob = new teacher();
            }
}

''')
    

def slip17():
    print('''
//slip no 17:
//Q1:
import java.util.Scanner;
import java.util.TreeSet;
public class a4
{
public static void main(String args[])
{
Scanner sc=new Scanner(System.in);
TreeSet<Object>ts=new TreeSet<>();
System.out.println("Enter how many numbers");
int n=sc.nextInt();
System.out.priintln("Enter the "+n+"numbers:");
for(int i=0;i<n;i++)
{
int num=sc.nextInt();
ts.add(num);
}
System.out.println("Numbers insorted order and without Duplication:"+ts);
sc.close();
}
}
//Q2:

import java.awt.GridLayout;

import java.awt.event.ActionEvent;

import java.util.logging.*;

import javax.swing.*;

public class slip17_2

{

    private JFrame frame;

    private JTextField tf;

    private JButton print;

    private Thread intThread;

   

    slip17_2() {

        frame = new JFrame("Integer printing App");

        frame.setSize(300, 200);

        frame.setLayout(new GridLayout(2,1));

       

        tf = new JTextField();

        print = new JButton("Print");

       

        frame.add(tf);

        frame.add(print);

       

        print.addActionListener((ActionEvent e) -> {

            tf.setText("");

            if(intThread == null || !intThread.isAlive()) {

                intThread = new Thread(new Runnable() {

                    @Override

                    public void run() {

                        while(true) {

                            for(int i=1; i<=100; i++) {

                                tf.setText(String.valueOf(i));

                                try {

                                    Thread.sleep(500);

                                } catch (InterruptedException ex) {

                                    Logger.getLogger(S17Q2.class.getName()).log(Level.SEVERE, null, ex);

                                }

                            }

                            tf.setText("");

                        }

                    }

                });

                intThread.start();

            }

        });

       

        frame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);

        frame.setVisible(true);

    }

   

    public static void main(String[] args) {

        new S17Q2();

    }

}


''')
    

def slip18():
    print('''
//slip 18
//Q1:
import java.util.Scanner;

import java.util.logging.*;

public class slip18_1

{

    public static void main(String[] args) {

        Scanner sc = new Scanner(System.in);

       

        System.out.println("Enter any string:");

        String str = sc.nextLine();

       

        Thread t = new Thread(() -> {

            for(int i=0; i<str.length(); i++) {

                String str2 = str.toLowerCase();

                char ch = str2.charAt(i);

                if(ch == 'a' || ch == 'e' || ch == 'i' || ch == 'o' || ch == 'u') {

                    System.out.println(ch);

                    try {

                        Thread.sleep(3000);

                    } catch (InterruptedException ex) {

                        Logger.getLogger(slip18_1.class.getName()).log(Level.SEVERE, null, ex);

                    }

                    System.out.println("3 seconds are passed....");

                }

            }

        });

       

        t.start();

    }

}
//Q2:
//servlet.java
import java.io.IOException;
import java.io.PrintWriter;
import javax.servlet.ServletException;
import javax.servlet.annotation.WebServlet;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;

@WebServlet("/StudentServlet")
public class StudentServlet extends HttpServlet {
    private static final long serialVersionUID = 1L;

    protected void doPost(HttpServletRequest request, HttpServletResponse response) 
            throws ServletException, IOException {
        // Set response content type
        response.setContentType("text/html");
        PrintWriter out = response.getWriter();

        // Retrieve form data
        String seatNo = request.getParameter("seatNo");
        String stuName = request.getParameter("stuName");
        String stuClass = request.getParameter("stuClass");
        String totalMarksStr = request.getParameter("totalMarks");

        // Parse the total marks
        int totalMarks = Integer.parseInt(totalMarksStr);

        // Calculate percentage
        double percentage = (totalMarks / 500.0) * 100;

        // Calculate grade based on percentage
        String grade;
        if (percentage >= 90) {
            grade = "A";
        } else if (percentage >= 80) {
            grade = "B";
        } else if (percentage >= 70) {
            grade = "C";
        } else if (percentage >= 60) {
            grade = "D";
        } else {
            grade = "F";
        }

        // Display the student details and result
        out.println("<html><body>");
        out.println("<h2>Student Details</h2>");
        out.println("<p>Seat No: " + seatNo + "</p>");
        out.println("<p>Name: " + stuName + "</p>");
        out.println("<p>Class: " + stuClass + "</p>");
        out.println("<p>Total Marks: " + totalMarks + "</p>");
        out.println("<p>Percentage: " + String.format("%.2f", percentage) + "%</p>");
        out.println("<p>Grade: " + grade + "</p>");
        out.println("</body></html>");
    }
}

//index.html
<!DOCTYPE html>
<html>
<head>
    <title>Student Details Form</title>
</head>
<body>
    <h2>Enter Student Details</h2>
    <form action="StudentServlet" method="post">
        <label for="seatNo">Seat No:</label>
        <input type="text" id="seatNo" name="seatNo"><br><br>
        
        <label for="stuName">Name:</label>
        <input type="text" id="stuName" name="stuName"><br><br>
        
        <label for="stuClass">Class:</label>
        <input type="text" id="stuClass" name="stuClass"><br><br>
        
        <label for="totalMarks">Total Marks (out of 500):</label>
        <input type="text" id="totalMarks" name="totalMarks"><br><br>
        
        <input type="submit" value="Submit">
    </form>
</body>
</html>
//first.xml
<web-app>
    <servlet>
        <servlet-name>StudentServlet</servlet-name>
        <servlet-class>StudentServlet</servlet-class>
    </servlet>

    <servlet-mapping>
        <servlet-name>StudentServlet</servlet-name>
        <url-pattern>/StudentServlet</url-pattern>
    </servlet-mapping>
</web-app>




''')
    

def slip19():
    print('''
//slip no 19:
//Q1:
import java.util.*;

public class slip19_1

{

    public static void main(String[] args) {

        List<Integer> l = new LinkedList<>();

        Scanner sc = new Scanner(System.in);

       

        System.out.println("How many values:");

        int n = sc.nextInt();

       

        System.out.println("Enter " + n + " values:");

        for(int i=0; i<n; i++)

            l.add(sc.nextInt());

       

        System.out.println("Negative integers are:");

        Iterator itr = l.iterator();

        while(itr.hasNext()) {

            int num = (int)itr.next();

            if(num < 0)

                System.out.println(num);

        }

    }

}
//Q2:
//database
CREATE DATABASE userdb;

USE userdb;

CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) NOT NULL,
    password VARCHAR(50) NOT NULL
);

INSERT INTO users (username, password) VALUES ('john', '12345'), ('alice', 'password');
//servlet.java
import java.io.IOException;
import java.io.PrintWriter;
import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.PreparedStatement;
import java.sql.ResultSet;
import javax.servlet.ServletException;
import javax.servlet.annotation.WebServlet;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;

@WebServlet("/LoginServlet")
public class LoginServlet extends HttpServlet {
    private static final String DB_URL = "jdbc:mysql://localhost:3306/UserDB";
    private static final String DB_USER = "root";  // Change as per your MySQL username
    private static final String DB_PASSWORD = "";  // Change as per your MySQL password

    protected void doPost(HttpServletRequest request, HttpServletResponse response) 
            throws ServletException, IOException {
        response.setContentType("text/html");
        PrintWriter out = response.getWriter();

        String username = request.getParameter("username");
        String password = request.getParameter("password");

        try {
            Class.forName("com.mysql.cj.jdbc.Driver");
            Connection conn = DriverManager.getConnection(DB_URL, DB_USER, DB_PASSWORD);

            String sql = "SELECT * FROM users WHERE username=? AND password=?";
            PreparedStatement pstmt = conn.prepareStatement(sql);
            pstmt.setString(1, username);
            pstmt.setString(2, password);

            ResultSet rs = pstmt.executeQuery();

            if (rs.next()) {
                out.println("<h2>Welcome, " + username + "!</h2>");
            } else {
                out.println("<h2 style='color:red;'>Invalid Username or Password!</h2>");
            }

            conn.close();
        } catch (Exception e) {
            out.println("<h2>Error: " + e.getMessage() + "</h2>");
        }
    }
}
//slip19.hrml
<!DOCTYPE html>
<html>
<head>
    <title>Login Page</title>
</head>
<body>
    <h2>Login</h2>
    <form action="LoginServlet" method="post">
        <label>Username:</label>
        <input type="text" name="username" required><br><br>
        <label>Password:</label>
        <input type="password" name="password" required><br><br>
        <input type="submit" value="Login">
    </form>
</body>
</html>
//web.xml`
<web-app xmlns="http://java.sun.com/xml/ns/javaee" version="3.0">
    <servlet>
        <servlet-name>LoginServlet</servlet-name>
        <servlet-class>LoginServlet</servlet>

''')
    

def slip20():
    print('''
//slip no 20
//Q1:
<%@page contentType="text/html" pageEncoding="UTF-8"%>

<!DOCTYPE html>

<html>

    <head>

        <meta http-equiv="Content-Type" content="text/html; charset=UTF-8">

        <title>JSP Page</title>

    </head>

    <body>

        <form action="slip20_1.jsp" method="post">

            Enter a number :<input type="text" name="num"><br>

            <input type="submit" value="show in words">

        </form>

       

        <%

        String numStr = request.getParameter("num");

           

        if(numStr != null && !numStr.isEmpty()) {

            int t = Integer.parseInt(numStr);

            int rev = 0, rem;

           

            // reverse the number

            while(t > 0) {

                rem = t % 10;

                rev = (rev * 10) + rem;

                t = t / 10;

            }

           

            t = rev;

            rev = 0;

            while(t > 0) {

                rem = t % 10;

                rev = (rev * 10) + rem;

                t = t / 10;

               

                switch(rem) {

                    case 0: out.println("zero");

                        break;

                    case 1: out.println("one");

                        break;

                    case 2: out.println("two");

                        break;

                    case 3: out.println("three");

                        break;

                    case 4: out.println("four");

                        break;

                    case 5: out.println("five");

                        break;

                    case 6: out.println("six");

                        break;

                    case 7: out.println("seven");

                        break;

                    case 8: out.println("eight");

                        break;

                    case 9: out.println("nine");

                        break;

                }

            }

        }

        %>

    </body>

</html>

//Q2:
import javax.swing.*;

import java.awt.*;

class TempleDrawing extends JFrame

{

    public TempleDrawing()

 {

        setTitle("Simple Temple Drawing");

        setSize(300, 300);

        setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);

        setLocationRelativeTo(null);

        TemplePanel templePanel = new TemplePanel();

        add(templePanel);

        setVisible(true);

    }

}

class TemplePanel extends JPanel

 {

    @Override

    protected void paintComponent(Graphics g)

 {

        super.paintComponent(g);

        drawTemple(g);

    }

    private void drawTemple(Graphics g)

  {

        g.setColor(Color.BLACK);

        g.fillRect(100, 100, 100, 100); // Main structure

       

        g.setColor(Color.WHITE);

        g.fillRect(130, 150, 40, 50); // Main Door

       

        g.setColor(Color.RED);

        int[] xPoints = {100, 150, 200}; // Triangle for roof

        int[] yPoints = {100, 50, 100};

        g.fillPolygon(xPoints, yPoints, 3);

        g.setColor(Color.ORANGE);

        g.fillRect(150, 40, 20, 10); // Flag

    }

}

public class slip20_2

{

    public static void main(String[] args)

 {

        SwingUtilities.invokeLater(() ->

        {

            new TempleDrawing();

        });

    }

}
''')
    

def slip21():
    print('''
//slip no 21:
//Q1:
import java.util.*;

public class slip21_1

{

    public static void main(String[] args) {

        List<String> l = new LinkedList<>();

        Scanner sc = new Scanner(System.in);

       

        System.out.println("How many subjects:");

        int n = sc.nextInt();

        sc.nextLine();

       

        System.out.println("Enter " + n + " subjects:");

        for(int i=0; i<n; i++)

            l.add(sc.nextLine());

       

        System.out.println("Subjects are:");

        Iterator itr = l.iterator();

        while(itr.hasNext()) {

            System.out.println(itr.next());

        }

    }

}
//Q2:
import java.io.*;
import java.lang.*;
class shared
{
int a;
Boolean valueChanged=false;
synchronized int get_data()
{
if(!valueChanged)
try
{
wait();
}
catch(InterruptedExecption e)
{
System.out.println("Interrupted");
}
System.out.println("Read:",+a);
valueChanged=false;

notify();
return a;
}
synchronized void put_data(int n)
{
if(valueChanged)
try
{
wait();
}
catch(IterruptedExecption e)
{
System.out.println("Interrupted");
}
this.a=n;
valueChanged=true;
System.out.println("Written :"+a);
notify();
}
}
class Producer implements Runnable
{
Shared ob;
Producer(Shared ob)
{
this.ob=ob;
new Thread(this,"Producer").start();
}
public void run()
{
int j=0;
while(true);
{
ob.put_data(j++);
}
}
}
class Consumer implements Runnable
{
Shared ob;
Consumer(Shared ob)
{
this.ob=ob;
new Thread(this,"Consumer").start();
}
public void run()
{
while(true)
{
ob.get_data();
}
}
}
class sync
{
public static void main (String args[])throws IOExecption
{
Shared ob=new Shared();
new Producer(ob);
new Consumer(ob);
System.out.println("Press cntl+c to stop");
}
}


''')
    

def slip22():
    print('''
//slip 22:
//Q1:
import java.sql.*;

import java.util.Scanner;

public class slip22_1

{

    private static void insert(Connection conn) throws SQLException {

        String sql = "insert into emp2 values (?, ?, ?)";

        PreparedStatement ps = conn.prepareStatement(sql);

       

        Scanner sc = new Scanner(System.in);

        System.out.println("Enter eno:");

        ps.setInt(1, sc.nextInt());

        sc.nextLine();

        System.out.println("Enter ename:");

        ps.setString(2, sc.nextLine());

        System.out.println("Enter salary:");

        ps.setFloat(3, sc.nextFloat());

       

        ps.executeUpdate();

    }

    private static void update(Connection conn) throws SQLException {

        Scanner sc = new Scanner(System.in);

        System.out.println("Enter eno:");

        int eno = sc.nextInt();

        sc.nextLine();

       

        System.out.println("Enter new  ename:");

        String ename = sc.nextLine();

       

        System.out.println("Enter new salary:");

        float salary = sc.nextFloat();

       

        String sql = "update emp2 set ename = '" + ename + "', salary = " + salary + " where eno = " + eno;

        Statement stmt = conn.createStatement();

        stmt.executeUpdate(sql);

    }

    private static void display(Connection conn) throws SQLException {

        String sql = "select * from emp2";

        Statement stmt = conn.createStatement();

        ResultSet rs = stmt.executeQuery(sql);

        System.out.println("Emp table data:");

        while (rs.next()) {

            System.out.println("eno: " + rs.getInt("eno"));

            System.out.println("ename: " + rs.getString("ename"));

            System.out.println("salary: " + rs.getFloat("salary"));

        }

    }

    public static void main(String[] args) throws SQLException {

        Scanner sc = new Scanner(System.in);

        Connection conn = DriverManager.getConnection("jdbc:postgresql://localhost:5432/postgres", "postgres", "postgres");

        int ch;

        do {

            System.out.println("Menu");

            System.out.println("1. Insert");

            System.out.println("2. Update");

            System.out.println("3. Display");

            System.out.println("4. Exit");

            System.out.println("-------------------------");

            System.out.println("Enter your choice:");

            ch = sc.nextInt();

            switch (ch) {

                case 1:

                    insert(conn);

                    break;

                case 2:

                    update(conn);

                    break;

                case 3:

                    display(conn);

                        break;

            }

        } while (ch != 4);

    }

}

//Q2:
<%@page contentType="text/html" pageEncoding="UTF-8"%>

<%@page import="java.time.LocalTime" %>

<!DOCTYPE html>

<html>

    <head>

        <meta http-equiv="Content-Type" content="text/html; charset=UTF-8">

        <title>JSP Page</title>

    </head>

    <body>

        <form action="slip22_2.jsp" method="post">

            Enter user name :<input type="text" name="user"><br>

            <input type="submit" value="greet">

        </form>

       

        <%

            String user = request.getParameter("user");

           

            if(user != null && !user.isEmpty()) {

                LocalTime currTime = LocalTime.now();

                int hour = currTime.getHour();

           

                if(hour >= 0 && hour < 12)

                    out.println("Good Morning " + user);

                else if(hour >= 12 && hour <= 18)

                    out.println("Good Afternoon " + user);

                else

                    out.println("Good Morning " + user);

            }

        %>

    </body>

</html>
''')
    

def slip23():
    print('''
//slip 23:
//Q1:
import java.util.Scanner;

import java.util.logging.*;

public class slip23_1

{

    public static void main(String[] args) {

        Scanner sc = new Scanner(System.in);

       

        System.out.println("Enter any string:");

        String str = sc.nextLine();

       

        Thread t = new Thread(() -> {

            for(int i=0; i<str.length(); i++) {

                String str2 = str.toLowerCase();

                char ch = str2.charAt(i);

                if(ch == 'a' || ch == 'e' || ch == 'i' || ch == 'o' || ch == 'u') {

                    System.out.println(ch);

                    try {

                        Thread.sleep(3000);

                    } catch (InterruptedException ex) {

                        Logger.getLogger(slip23_1.class.getName()).log(Level.SEVERE, null, ex);

                    }

                    System.out.println("3 seconds are passed....");

                }

            }

        });

       

        t.start();

    }

}

//Q2:
import java.util.*;

public class StudentList {
    public static void main(String[] args) {
        if (args.length == 0) {
            System.out.println("Usage: java StudentList <student1> <student2> ... <studentN>");
            return;
        }

        // Using ArrayList to store student names
        List<String> studentNames = new ArrayList<>();

        // Adding names from command line arguments
        Collections.addAll(studentNames, args);

        // Display using Iterator (Forward Traversal)
        System.out.println("\nDisplaying Student Names using Iterator:");
        Iterator<String> iterator = studentNames.iterator();
        while (iterator.hasNext()) {
            System.out.println(iterator.next());
        }

        // Display using ListIterator (Forward & Backward Traversal)
        System.out.println("\nDisplaying Student Names using ListIterator (Forward):");
        ListIterator<String> listIterator = studentNames.listIterator();
        while (listIterator.hasNext()) {
            System.out.println(listIterator.next());
        }

        System.out.println("\nDisplaying Student Names using ListIterator (Backward):");
        while (listIterator.hasPrevious()) {
            System.out.println(listIterator.previous());
        }
    }
}

''')
    

def slip24():
    print('''
//slip no 24:
//Q1:
import javax.swing.*;

class TextScrolling extends JFrame implements Runnable {

    private JLabel label;

    private String text;

    private Thread thread;

    public TextScrolling(String text) {

        this.text = text;

        label = new JLabel(text);

        add(label);

        setSize(300, 100);

        setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);

        setVisible(true);

    }

    public void startScrolling() {

        thread = new Thread(this);

        thread.start();

    }

    @Override

    public void run() {

        try {

            while (true) {

                String labelText = label.getText();

                labelText = labelText.substring(1) + labelText.charAt(0);

                label.setText(labelText);

                Thread.sleep(200); // Adjust scrolling speed

            }

        } catch (InterruptedException e) {

            e.printStackTrace();

        }

    }    

}

public class slip24_1

{

    public static void main(String[] args) {

        SwingUtilities.invokeLater(() -> {

            TextScrolling ts = new TextScrolling("Hello, this text is scrolling continuously!");

            ts.startScrolling();

        });

    }

}
//Q2:
//slip.jsp
import javax.swing.*;

class TextScrolling extends JFrame implements Runnable {

    private JLabel label;

    private String text;

    private Thread thread;

    public TextScrolling(String text) {

        this.text = text;

        label = new JLabel(text);

        add(label);

        setSize(300, 100);

        setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);

        setVisible(true);

    }

    public void startScrolling() {

        thread = new Thread(this);

        thread.start();

    }

    @Override

    public void run() {

        try {

            while (true) {

                String labelText = label.getText();

                labelText = labelText.substring(1) + labelText.charAt(0);

                label.setText(labelText);

                Thread.sleep(200); // Adjust scrolling speed

            }

        } catch (InterruptedException e) {

            e.printStackTrace();

        }

    }    

}

public class slip24_1

{

    public static void main(String[] args) {

        SwingUtilities.invokeLater(() -> {

            TextScrolling ts = new TextScrolling("Hello, this text is scrolling continuously!");

            ts.startScrolling();

        });

    }

}
//slip.html
<!DOCTYPE html>
<html>
<head>
    <title>Login Page</title>
</head>
<body>
    <h2>Login</h2>
    <form action="login.jsp" method="post">
        <label>Username:</label>
        <input type="text" name="username" required><br><br>
        <label>Password:</label>
        <input type="password" name="password" required><br><br>
        <input type="submit" value="Login">
    </form>
</body>
</html>
//login.html
<!DOCTYPE html>
<html>
<head>
    <title>Login Successful</title>
</head>
<body>
    <h2 style="color: green;">Login Successfully</h2>
</body>
</html>
//error.html
<!DOCTYPE html>
<html>
<head>
    <title>Login Failed</title>
</head>
<body>
    <h2 style="color: red;">Login Failed</h2>
</body>
</html>
''')
    

def slip25():
    print('''
//slip no 25:
//Q1:
//slip.jsp
<%@ page language="java" contentType="text/html; charset=UTF-8" pageEncoding="UTF-8" %>
<%
    // Get the name and age from the form
    String name = request.getParameter("name");
    String ageStr = request.getParameter("age");
    int age = 0;
    String message = "";
    
    // Check if age is a valid integer
    try {
        if (ageStr != null && !ageStr.isEmpty()) {
            age = Integer.parseInt(ageStr);
        }
    } catch (NumberFormatException e) {
        message = "Please enter a valid age.";
    }
    
    // Check eligibility
    if (age >= 18) {
        message = name + ", you are eligible to vote!";
    } else if (age > 0) {
        message = name + ", you are not eligible to vote.";
    } else {
        message = "Invalid age entered.";
    }
%>

<!DOCTYPE html>
<html>
<head>
    <title>Voter Eligibility Check</title>
</head>
<body>
    <h2>Voter Eligibility Check</h2>
    <p><%= message %></p>
    <br>
    <a href="index.html">Back to Voter Input</a>
</body>
</html>
//erdfj.html
<!DOCTYPE html>
<html>
<head>
    <title>Voter Eligibility Form</title>
</head>
<body>
    <h2>Enter Voter Details</h2>
    <form action="voterEligibility.jsp" method="post">
        <label for="name">Name:</label>
        <input type="text" id="name" name="name" required><br><br>
        
        <label for="age">Age:</label>
        <input type="number" id="age" name="age" required><br><br>
        
        <input type="submit" value="Check Eligibility">
    </form>
</body>
</html>
//Q2:
import java.awt.BorderLayout;

import java.awt.GridLayout;

import java.awt.event.ActionEvent;

import java.sql.Connection;

import java.sql.DriverManager;

import java.sql.SQLException;

import java.sql.Statement;

import java.util.logging.Level;

import java.util.logging.Logger;

import javax.swing.JButton;

import javax.swing.JFrame;

import javax.swing.JLabel;

import javax.swing.JPanel;

import javax.swing.JTextField;

public class slip25_2

{

    JFrame frame;

    JButton b1, b2, b3;

    JTextField tf;

   

    slip25_2() throws SQLException {

        frame = new JFrame("DB App");

        frame.setLayout(new BorderLayout());

        frame.setSize(600, 100);

       

        JPanel p1 = new JPanel();

        JPanel p2 = new JPanel();

       

        tf = new JTextField();

        p1.setLayout(new GridLayout(1, 2));

        p1.add(new JLabel("Type your DDL query:"));

        p1.add(tf);

       

        b1 = new JButton("Create Table");

        b2 = new JButton("Alter Table");

        b3 = new JButton("Drop Table");

        p2.setLayout(new GridLayout(1, 3));

        p2.add(b1);

        p2.add(b2);

        p2.add(b3);

       

        Connection conn = DriverManager.getConnection("jdbc:postgresql://localhost:5432/postgres", "postgres", "postgres");

       

        b1.addActionListener((ActionEvent e) -> {

            try {

                create(conn);

            } catch (SQLException ex) {

                Logger.getLogger(S25Q2.class.getName()).log(Level.SEVERE, null, ex);

            }

        });

        b2.addActionListener((ActionEvent e) -> {

            try {

                alter(conn);

            } catch (SQLException ex) {

                Logger.getLogger(S25Q2.class.getName()).log(Level.SEVERE, null, ex);

            }

        });

        b3.addActionListener((ActionEvent e) -> {

            try {

                drop(conn);

            } catch (SQLException ex) {

                Logger.getLogger(S25Q2.class.getName()).log(Level.SEVERE, null, ex);

            }

        });

       

        frame.add(p1, BorderLayout.CENTER);

        frame.add(p2, BorderLayout.SOUTH);

        frame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);

        frame.setVisible(true);

    }

   

    private void create(Connection conn) throws SQLException {

        String sql = tf.getText();        

        Statement stmt = conn.createStatement();

        stmt.execute(sql);

    }

    private void alter(Connection conn) throws SQLException {

        String sql = tf.getText();        

        Statement stmt = conn.createStatement();

        stmt.execute(sql);

    }

    private void drop(Connection conn) throws SQLException {

        String sql = tf.getText();        

        Statement stmt = conn.createStatement();

        stmt.execute(sql);

    }

   

    public static void main(String[] args) throws SQLException {

        new S25Q2();

    }

}

''')
    

def slip26():
    print('''
//slip No 26:
//Q1:
CREATE DATABASE EmployeeDB;
USE EmployeeDB;

CREATE TABLE employees (
    ENo INT PRIMARY KEY,
    EName VARCHAR(50) NOT NULL,
    Salary DOUBLE NOT NULL
);

-- Insert sample data
INSERT INTO employees (ENo, EName, Salary) VALUES (101, 'Alice', 50000);
INSERT INTO employees (ENo, EName, Salary) VALUES (102, 'Bob', 60000);
INSERT INTO employees (ENo, EName, Salary) VALUES (103, 'Charlie', 70000);

import java.sql.*;

public class DeleteEmployee {
    public static void main(String[] args) {
        // Ensure an Employee ID is passed as a command-line argument
        if (args.length != 1) {
            System.out.println("Usage: java DeleteEmployee <Employee_ID>");
            return;
        }

        int empId = Integer.parseInt(args[0]); // Convert command-line argument to integer

        // Database credentials
        String url = "jdbc:mysql://localhost:3306/your_database"; // Replace 'your_database' with actual database name
        String user = "your_username"; // Replace with your DB username
        String password = "your_password"; // Replace with your DB password

        // SQL query to delete employee
        String sql = "DELETE FROM employees WHERE ENo = ?";

        try (
            // Load MySQL JDBC Driver
            Connection conn = DriverManager.getConnection(url, user, password);
            PreparedStatement pstmt = conn.prepareStatement(sql)
        ) {
            pstmt.setInt(1, empId); // Set Employee ID parameter

            int rowsAffected = pstmt.executeUpdate(); // Execute delete query

            if (rowsAffected > 0) {
                System.out.println("Employee with ID " + empId + " deleted successfully.");
            } else {
                System.out.println("No employee found with ID " + empId);
            }
        } catch (SQLException e) {
            e.printStackTrace();
        }
    }
}
//Q2:
//sun.jsp
<%@ page language="java" contentType="text/html; charset=UTF-8" pageEncoding="UTF-8" %>
<!DOCTYPE html>
<html>
<head>
    <title>Sum of First and Last Digit</title>
</head>
<body>

    <h2>Calculate Sum of First and Last Digit</h2>

    <form action="sum.jsp" method="get">
        Enter a Number: <input type="text" name="num" required>
        <input type="submit" value="Calculate">
    </form>

    <%
        // Get number from request
        String numStr = request.getParameter("num");
        if (numStr != null && numStr.matches("\\d+")) { // Ensure input is a valid number
            int num = Integer.parseInt(numStr);

            // Extract first and last digit
            int lastDigit = num % 10;  // Get last digit
            int firstDigit = Integer.parseInt(String.valueOf(numStr.charAt(0))); // Get first digit

            int sum = firstDigit + lastDigit;

            // Display sum in red color with font size 18
    %>
            <h3 style="color: red; font-size: 18px;">Sum of First and Last Digit: <%= sum %></h3>
    <%
        } else if (numStr != null) {
    %>
            <p style="color: red;">Invalid Input! Please enter a valid number.</p>
    <%
        }
    %>

</body>
</html>


''')
    

def slip27():
    print('''
//Slip no 27:
// Q1:
import java.awt.BorderLayout;

import java.sql.*;

import javax.swing.*;

class CollegeTable {

    private JFrame frame;

    private JTable table;

   

    CollegeTable() throws SQLException {

        frame = new JFrame("Project Table");

        frame.setLayout(new BorderLayout());

        frame.setSize(600, 150);

        Connection conn = DriverManager.getConnection("jdbc:postgresql://localhost:5432/postgres", "postgres", "postgres");

       

        String[] colNames = {"cid", "cname", "address", "year"};

        String[][] data = retriveData(conn);

       

        table = new JTable(data, colNames);

        JScrollPane scrPane = new JScrollPane(table);

       

        frame.getContentPane().add(scrPane, BorderLayout.CENTER);        

        frame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);

        frame.setVisible(true);

    }

    private String[][] retriveData(Connection conn) throws SQLException {

        String sql = "select * from college";

        Statement stmt = conn.createStatement(ResultSet.TYPE_SCROLL_INSENSITIVE, ResultSet.CONCUR_READ_ONLY);

        ResultSet rs = stmt.executeQuery(sql);

        ResultSetMetaData rsmd = rs.getMetaData();

        int noCol = rsmd.getColumnCount();

        rs.last();

        int noRow = rs.getRow();

        rs.beforeFirst();

        String[][] data = new String[noRow][noCol];

        int rowCnt = 0;

        while (rs.next()) {

            for (int i = 1; i <= noCol; i++)

                data[rowCnt][i - 1] = rs.getString(i);

            rowCnt++;

        }

        return data;

    }

}

public class slip27_1

{

    public static void main(String[] args) throws SQLException {

        new CollegeTable();

    }

}

//Q2:
//.jsp
import java.io.IOException;
import java.io.PrintWriter;
import javax.servlet.ServletException;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;
import javax.servlet.http.HttpSession;

public class SessionTimeoutServlet extends HttpServlet {
    protected void doGet(HttpServletRequest request, HttpServletResponse response) throws ServletException, IOException {
        response.setContentType("text/html");
        PrintWriter out = response.getWriter();
        
        // Get session or create a new one
        HttpSession session = request.getSession(true);

        // Retrieve timeout value from request (default to 5 minutes if not provided)
        String timeoutParam = request.getParameter("timeout");
        int timeout = (timeoutParam != null && timeoutParam.matches("\\d+")) ? Integer.parseInt(timeoutParam) : 5;

        // Set session timeout in minutes
        session.setMaxInactiveInterval(timeout * 60);

        // Display confirmation message
        out.println("<html><head><title>Session Timeout</title></head><body>");
        out.println("<h2>Session Timeout Updated</h2>");
        out.println("<p>Session Timeout is now set to <b>" + timeout + " minutes</b>.</p>");

        // Form to update session timeout
        out.println("<form action='SessionTimeoutServlet' method='get'>");
        out.println("Set New Timeout (minutes): <input type='text' name='timeout' required>");
        out.println("<input type='submit' value='Update Timeout'>");
        out.println("</form>");

        out.println("</body></html>");
    }
}
web.xml
<web-app xmlns="http://java.sun.com/xml/ns/javaee" version="3.0">
    <servlet>
        <servlet-name>SessionTimeoutServlet</servlet-name>
        <servlet-class>SessionTimeoutServlet</servlet-class>
    </servlet>
    <servlet-mapping>
        <servlet-name>SessionTimeoutServlet</servlet-name>
        <url-pattern>/SessionTimeoutServlet</url-pattern>
    </servlet-mapping>
</web-app>

''')
    

def slip28():
    print('''
//Slip no 28:
//Q1:
//reverse.jsp
<%@ page language="java" contentType="text/html; charset=UTF-8" pageEncoding="UTF-8" %>
<!DOCTYPE html>
<html>
<head>
    <title>Reverse a String</title>
</head>
<body>

    <h2>Enter a String to Reverse</h2>

    <form action="reverse.jsp" method="post">
        Enter String: <input type="text" name="inputString" required>
        <input type="submit" value="Reverse">
    </form>

    <%
        // Retrieve input string from request
        String input = request.getParameter("inputString");

        if (input != null && !input.isEmpty()) {
            // Reverse the string using StringBuilder
            String reversed = new StringBuilder(input).reverse().toString();
    %>
            <h3>Original String: <%= input %></h3>
            <h3>Reversed String: <%= reversed %></h3>
    <%
        }
    %>

</body>
</html>
//Q2:
//thread.java
class MyThread extends Thread {
    public void run() {
        // Get the name of the currently executing thread
        System.out.println("Currently Executing Thread: " + Thread.currentThread().getName());
    }
}

public class ThreadNameExample {
    public static void main(String[] args) {
        // Create multiple threads
        MyThread t1 = new MyThread();
        MyThread t2 = new MyThread();
        MyThread t3 = new MyThread();

        // Set thread names
        t1.setName("Thread-1");
        t2.setName("Thread-2");
        t3.setName("Thread-3");

        // Start the threads
        t1.start();
        t2.start();
        t3.start();
    }
}

''')
    

def slip29():
    print('''
//Slip no 29
//Q1:
import java.sql.*;

public class slip29_1

{

    public static void main(String[] args) throws SQLException {

        Connection conn = DriverManager.getConnection("jdbc:postgresql://localhost:5432/postgres", "postgres", "postgres");

       

        String sql = "select * from donar";

       

        Statement stmt = conn.createStatement();

        stmt.executeQuery(sql);

       

        ResultSet rs = stmt.getResultSet();

        ResultSetMetaData rsmd = rs.getMetaData();

       

        int colCnt = rsmd.getColumnCount();

        System.out.println("Donar table Meta Data:");

        for(int i=1; i<colCnt; i++) {

            String colName = rsmd.getColumnName(i);

            String colType = rsmd.getColumnTypeName(i);

            int colSize = rsmd.getColumnDisplaySize(i);

           

            System.out.println(colName + " " + colType + "(" + colSize + ")");

        }

    }

}
//Q2:
import java.util.*;

public class slip29_2

{

    public static void main(String[] args) {

        List<Integer> l = new LinkedList<>();

        Scanner sc = new Scanner(System.in);

       

        int ch;

       

        do {

            System.out.println("Menu");

            System.out.println("1. Insert at head");

            System.out.println("2. Delete tail.");

            System.out.println("3. Display size");

            System.out.println("4. Exit");

           

            System.out.println("------------------------------");

            System.out.println("Enter your choice:");

            ch = sc.nextInt();

            System.out.println();

           

            switch(ch) {

                case 1: System.out.println("Enter a number:");

                    l.addFirst(sc.nextInt());

                    break;

                case 2: l.removeLast();

                    break;

                case 3:

                    System.out.println("Size : " + l.size() + "\n" + l);

                    break;

                default: System.out.println("Invalid choice.");

            }

            System.out.println("-------------------------------");

        } while(ch != 4);

    }

}


''')
    

def slip30():
    print('''
//Slip no 30
//Q1:
import javax.swing.*;

import java.awt.*;

class IndianFlag extends JFrame {

    public IndianFlag() {

        setTitle("Simple Temple Drawing");

        setSize(300, 300);

        setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);

        setLocationRelativeTo(null);

        FlagPanel flagPanel = new FlagPanel();

        add(flagPanel);

        setVisible(true);

    }

}

class FlagPanel extends JPanel {

    @Override

    protected void paintComponent(Graphics g) {

        super.paintComponent(g);

        drawFlag(g);

    }

    private void drawFlag(Graphics g) {

        g.setColor(Color.ORANGE);

        g.fillRect(50, 50, 200, 50);

       

        g.setColor(Color.WHITE);

        g.fillRect(50, 100, 200, 50);

       

        g.setColor(Color.GREEN);

        g.fillRect(50, 150, 200, 50);

       

    }

}

public class slip30_1

{

    public static void main(String[] args) {

        SwingUtilities.invokeLater(() -> {

            new IndianFlag();

        });

    }

}

//Q2:
CREATE TABLE Teacher (
    TID INT PRIMARY KEY,
    TName VARCHAR(100),
    Salary DECIMAL(10,2)
);
INSERT INTO Teacher (TID, TName, Salary) VALUES
(1, 'Alice', 50000.00),
(2, 'Bob', 55000.00),
(3, 'Charlie', 60000.00);

import java.sql.*;

public class ScrollableResultSetExample {
    public static void main(String[] args) {
        // Database connection details
        String url = "jdbc:mysql://localhost:3306/your_database"; // Change 'your_database' to actual database name
        String user = "your_username"; // Change to your MySQL username
        String password = "your_password"; // Change to your MySQL password

        // SQL Query
        String query = "SELECT * FROM Teacher";

        try {
            // Load MySQL JDBC Driver
            Class.forName("com.mysql.cj.jdbc.Driver");

            // Establish Connection
            Connection conn = DriverManager.getConnection(url, user, password);

            // Create a Scrollable & Updatable ResultSet
            Statement stmt = conn.createStatement(
                    ResultSet.TYPE_SCROLL_INSENSITIVE, 
                    ResultSet.CONCUR_READ_ONLY
            );

            // Execute Query
            ResultSet rs = stmt.executeQuery(query);

            System.out.println("Displaying Teacher Table Data:");

            // Move to First Row
            if (rs.first()) {
                System.out.println("First Record: " + rs.getInt("TID") + " | " + rs.getString("TName") + " | " + rs.getDouble("Salary"));
            }

            // Move to Last Row
            if (rs.last()) {
                System.out.println("Last Record: " + rs.getInt("TID") + " | " + rs.getString("TName") + " | " + rs.getDouble("Salary"));
            }

            // Move to Second Row
            if (rs.absolute(2)) {
                System.out.println("Second Record: " + rs.getInt("TID") + " | " + rs.getString("TName") + " | " + rs.getDouble("Salary"));
            }

            // Move Backward to Previous Row
            if (rs.previous()) {
                System.out.println("Previous Record (before second): " + rs.getInt("TID") + " | " + rs.getString("TName") + " | " + rs.getDouble("Salary"));
            }

            // Close Resources
            rs.close();
            stmt.close();
            conn.close();
        } catch (Exception e) {
            e.printStackTrace();
        }
    }
}

''')