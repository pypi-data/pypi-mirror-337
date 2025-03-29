# texts.py
import pyperclip as pc
def copyprint(a):
    print(a)
    pc.copy(a)
def print_cp1():
    a=r"""
#include <conio.h>
#include <stdio.h>

void main()

{

char Operator;

float numl, num2, result = 0;

printf("Enter an Operator (+, -, *, /) :
 ");

scanf("%c", &Operator);

printf("Enter the Values for two Operands: numl and num2: 
 ");

scanf("%f%f", &numl, &num2);

switch(Operator)

{

case '+':

result = num1 + num2;break;

case '-':

result = numl -

num2;break;

case

result = num1* num2;break;

case '/:

result = num1/num2;break;

default:

printf("
 You have enetered an Invalid Operator ");

}

printf("
 The result of %f%c %f= %f", numl, Operator, num2, result);

getch();

}"""
    print(a)
    pc.copy(a)


def print_cp2():
    a=r"""
#include <stdio.h> 
#include <conio.h> 
#include <math.h> 
#include <stdlib.h> 
void main() 
{ 
float a,b,c,root1,root2,realp,imagp,disc; 
clrscr(); 
printf("\n Enter the value of coefficient a: "); 
scanf("%f",&a); 
 
if(a == 0) 
{ 
printf("\n Invalid input...Retry again"); 
exit(0); 
} 
printf(" Enter the value of coefficients b and c:\n "); 
scanf("%f%f",&b,&c); 
disc = b*b-4*a*c; // compute discriminant 
 
if(disc == 0) 
{ 
printf("The roots are real and equal\n"); 
root1 = root2 = -b / (2.0*a); 
printf(" Root1 = Root2 = %.2f\n", root1); 
} 
else 
{ 
if(disc > 0) 
{ 
printf("The roots are real and distinct\n"); 
root1 = (-b + sqrt(disc))/(2.0*a); 
root2 = (-b - sqrt(disc))/(2.0*a); 
printf("Root1 = %.2f\n", root1); 
printf("Root2 = %.2f\n", root2); 
} 
else 
{ 
printf("The roots are complex\n"); 
realp = -b/(2.0*a); 
disc=-disc; 
imagp = sqrt(disc)/(2.0*a); 
 
printf("Root1 = %.2f + i%.2f\n",realp,imagp); 
printf("Root2 = %.2f - i %.2f\n",realp, imagp); 
} 
} 
getch(); 
} """
    print(a)
    pc.copy(a)


def print_cp3():
  a=r"""
#include <stdio.h> 
#include<conio.h> 
 void main() 
{ 
char name[10];  
float unit, amt; 
 clrscr(); 
printf("Enter your name and unit Consumed:");  
scanf("%s %f",name,&unit); 
if(unit<=200)  
amt=unit*0.80+100; 
else if((unit>200)&&(unit<=300))  
amt=200*0.80+((unit-200)*0.90)+100; 
else 
amt=200*0.80+100*0.90+((unit-300)*1)+100; 
if(amt>400)  
amt=1.15*amt; 
printf("Name: %s\n Unit=%f \n charge=%f ",name,unit,amt);  
getch(); 
}"""
  print(a)
  pc.copy(a)


def print_cp4():
  a=r"""
#include <stdio.h> 
#include <conio.h> 
void main() 
{ 
int i,j,n; 
clrscr( ); 
printf("Input number of rows : "); 
scanf("%d",&n); 
for(i=0; i<=n;i++) 
{ 
for(j=1;j<=n-i;j++) 
{ 
printf(" "); 
} 
for(j=1;j<=i;j++) 
{ 
printf("%d",j); 
} 
for(j=i-1;j>=1;j--) 
{ 
printf("%d",j); 
} 
printf("\n"); 
} 
getch(); 
} """
  print(a)
  pc.copy(a)

def print_cp5():
   a=r"""
#include <stdio.h> 
#include <conio.h> 
void main() 
{ 
int n, a[100], i, key, high, low, mid, loc=-1; 
clrscr( ); 
printf("Enter the size of the array\n"); 
scanf("%d",&n); 
printf("Enter the elements of array in sorted order\n"); 
for(i=0;i<n;i++) 
scanf("%d",&a[i]); 
printf("Enter the key element to be searched\n"); 
scanf("%d",&key); 
low=0; 
high=n-1; 
while(low<=high) 
{ 
mid=(low+high)/2; 
if(key= =a[mid]) 
{ 
loc = mid+1; 
break; 
} 
else 
{ 
if(key<a[mid]) 
high=mid-1; 
else 
low=mid+1; 
} 
} 
if(loc>0) 
printf("\n The element %d is found at %d ",key,loc); 
 
else 
printf("\nThe search is unsuccessful"); 
getch(); 
} """
   print(a)
   pc.copy(a)

def print_cp6():
   a=r"""
#include<stdio.h> 
#include<conio.h> 
void main() 
{ 
int a[5][5],b[5][5],c[5][5],m,n,p,q,i,j,k; 
clrscr(); 
printf("Enter the size of first matrix\n"); 
scanf("%d %d",&m,&n); 
printf("Enter the size of second matrix\n"); 
scanf("%d %d",&p,&q); 
if(n!=p) 
printf(“Matrix multiplication is not possible”); 
else 
{ 
printf("Enter the elements of first matrix\n"); 
for(i=0;i<m;i++) 
for(j=0;j<n;j++) 
scanf("%d",&a[i][j]); 
printf("Enter the elements of the second matrix\n"); 
for(i=0;i<p;i++) 
for(j=0;j<q;j++) 
scanf("%d",&b[i][j]); 
for(i=0;i<m;i++) 
for(j=0;j<q;j++) 
{ 
c[i][j]=0; 
for(k=0;k<n;k++) 
c[i][j]=c[i][j]+a[i][k]*b[k][j]; 
} 
printf("\n A- matrix is\n");  
for(i=0;i<m;i++) 
{ 
for(j=0;j<n;j++) 
printf("%d\t",a[i][j]); 
printf("\n"); 
} 
printf("\n B- matrix is\n"); 
for(i=0;i<p;i++) 
{ 
for(j=0;j<q;j++) 
printf("%d\t",b[i][j]); 
printf("\n"); 
} 
printf("The product of two matrices is\n"); 
for(i=0;i<m;i++) 
{ 
for(j=0;j<q;j++) 
printf("%d\t",c[i][j]); 
printf("\n"); 
} 
} 
getch(); 
}"""
   print(a)
   pc.copy(a)

def print_cp7():
   a=r"""
#include<stdio.h> 
#include<conio.h> 
#include<stdlib.h> 
#include<math.h> 
int fact(int m) 
{ 
int i,f=1; 
for(i=1;i<=m;i++) 
{ 
f=f*i; 
} 
return f; 
} 
void main() 
{ 
int x,n,i; 
float rad, res, sum=0; 
clrscr(); 
printf("Enter degree\n"); 
scanf("%d",&x); 
printf("Enter number of terms\n"); 
scanf("%d",&n); 
rad=x*3.14/180; 
for(i=1;i<=n;i+=2) 
{ 
if ((i-1)%4==0) 
sum=sum+pow(rad,i)/fact(i); 
else 
sum=sum-pow(rad,i)/fact(i); 
} 
printf("Calculate sin(%d) = %f", x,sum); 
printf("\nLibrary sin(%d) = %f", x,sin(rad)); 
getch(); 
}"""
   print(a)
   pc.copy(a)


def print_cp8():
   a=r"""
#include<stdio.h> 
#include<conio.h> 
void main() 
{ 
int n,i,j,a[10],temp; 
clrscr(); 
printf("Enter the no. of elements : \n"); 
scanf("%d",&n); 
printf("Enter the array elements \n"); 
for(i = 0 ; i < n ; i++) 
scanf("%d",&a[i]); 
printf("The original elements are \n"); 
for(i = 0 ; i < n ; i++) 
printf("%d ",a[i]); 
for(i = 0 ; i < n-1 ; i++) 
{ 
for(j = 0 ; j< (n-i)-1; j++) 
{ 
if(a[j] > a[j+1]) 
{ 
temp = a[j]; 
a[j] = a[j+1]; 
a[j+1] = temp; 
} 
} 
} 
printf("\n The Sorted elements are \n"); 
for(i = 0 ; i < n ; i++) 
printf("%d ",a[i]); 
getch(); 
}"""
   print(a)
   pc.copy(a)

def print_cp9():
   a=r"""
#include<stdio.h> 
#include<conio.h> 
int strlength(char str1[50]); 
void strconcat(char str1[50],char str2[50]); 
int strcompare(char str1[50],char str2[50]); 
int strlength(char str[50]) 
{ 
int i=0; 
while(str[i]!=’\0') 
i++; 
return i; 
} 
void strconcat(char str1[50],char str2[50]) 
{ 
int i=0,l; 
l=strlength(str1); 
while(str2[i]!=’\0') 
{ 
str1[l+i]=str2[i];
i++; 
} 
str1[l+i]=’\0'; 
} 
int strcompare(char str1[50],char str2[50]) 
{ 
int i=0, k; 
while(str1[i]==str2[i]) 
{ 
if(str1[i]==’\0') 
break; 
i++; 
} 
k=str1[i]-str2[i]; 
return k; 
} 
void main() 
{ 
char source1[50],source2[50],dest[50]; 
int length1,length2,k; 
clrscr(); 
printf(“\n Enter the source string 1:”); 
gets(source1); 
printf(“\n Enter the source string 2:”); 
gets(source2); 
length1=strlength(source1); 
length2=strlength(source2); 
printf(“\n string length of string 1 is %d”,length1); 
printf(“\n string length of string 2 is %d”,length2); 
k=strcompare(source1,source2); 
if(k==0) 
printf(“\n Both string are same”);
else 
printf(“\n Both string are different”); 
strconcat(source1,source2); 
printf(“\n concatenated string is “); 
puts(source1); 
getch(); 
}"""
   print(a)
   pc.copy(a)


def print_cp10():
   a=r"""
#include<stdio.h> 
#include<conio.h> 
struct student 
{ 
char usn[10]; 
char name[10]; 
int m1,m2,m3; 
float avg, total; 
}; 
void main() 
{ 
struct student s[20]; 
int n,i; 
float tavg,sum=0.0; 
clrscr(); 
printf("Enter the number of students"); 
scanf("%d",&n); 
for(i=0;i<n;i++) 
{ 
printf("Enter the detail of %d students\n",i+1); 
printf("\n Enter USN="); 
scanf("%s",s[i].usn); 
printf("\n Enter Name="); 
scanf("%s",s[i].name); 
printf("\nEnter the three subjects marks\n"); 
scanf("%d%d%d",&s[i].m1,&s[i].m2,&s[i].m3); 
s[i].total=s[i].m1+s[i].m2+s[i].m3; 
s[i].avg=s[i].total/3; 
} 
for(i=0;i<n;i++) 
{
if(s[i].avg>=35) 
printf("\n %s has scored above the average marks",s[i].name); 
else 
printf("\n %s has scored below the average marks",s[i].name); 
} 
getch(); 
}"""
   print(a)
   pc.copy(a)


def print_cp11():
   a=r"""
#include<stdio.h> 
#include<conio.h> 
#include<math.h> 
int main() 
{ 
int n , i; 
float x[20],sum,mean; 
float variance , deviation; 
clrscr(); 
printf("Enter the value of n \n"); 
scanf("%d",&n); 
printf("enter %d real values \n",n); 
for (i=0;i<n;i++) 
{ 
scanf("%f",(x+i)); 
} 
sum=0; 
for(i=0;i<n;i++) 
{ 
sum= sum+*(x+i); 
} 
printf("sum=%f\n",sum); 
mean=sum/n; 
sum=0; 
for(i=0;i<n;i++) 
{ 
sum=sum+(*(x+i)-mean)*(*(x+i)-mean); 
} 
variance=sum/n; 
deviation=sqrt(variance); 
printf("mean(Average)=%f\n",mean); 
printf("variance=%f\n",variance); 
printf("standard deviation=%f\n",deviation); 
getch(); 
}"""
   print(a)
   pc.copy(a)


def print_cp12():
   a=r"""
#include <stdio.h> 
#include <stdlib.h> 
#include <conio.h> 
void main() 
{ 
FILE *fptr1, *fptr2; 
char ch, fname1[20], fname2[20]; 
clrscr(); 
 
printf("\n\n Copy a file in another name :\n"); 
printf(" \n"); 
 
printf(" Input the source file name : "); 
scanf("%s",fname1); 
 
fptr1=fopen(fname1, "r"); 
if(fptr1==NULL) 
{ 
printf(" File does not found or error in opening.!!"); 
exit(1); 
} 
printf(" Input the new file name : "); 
scanf("%s",fname2); 
fptr2=fopen(fname2, "w"); 
if(fptr2==NULL) 
{ 
printf(" File does not found or error in opening.!!"); 
fclose(fptr1); 
exit(2); 
} 
while(1) 
{ 
ch=fgetc(fptr1); 
if(ch==EOF) 
{ 
break; 
} 
else
{ 
fputc(ch, fptr2); 
} 
} 
printf(" The file %s copied successfully in the file %s. \n\n",fname1,fname2); 
fclose(fptr1); 
fclose(fptr2); 
getchar(); 
}"""
   print(a)
   pc.copy(a)

#html programs
def print_h1():
   a=r"""<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.1//EN" "http://www.w3.org/TR/xhtml11/DTD/xhtml11.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="en">
<head>
<title>SAMPLE XHTML PAGE</title>
<meta name="author" content="Putta" />
<meta name="date" content="2023-02-17T04:15:01+0530" />
<meta http-equiv="content-type" content="text/html; charset=UTF-8"/>
<meta http-equiv="content-type" content="application/xhtml+xml; charset=UTF-8"/>
<meta http-equiv="content-style-type" content="text/css"/>
<meta http-equiv="expires" content="0"/>
</head>
<body>

<style>
body {
  background-image: url("image.png");
  background-repeat: no-repeat;
  background-position: right bottom;
  background-attachment: fixed;
}
</style>

<h4>Paragraph</h4>
<p>
<b><i>All that glitters is not gold</i></b> is an aphorism stating that not everything that looks precious or true turns out to be so. 
While early expressions of the idea are known from at least the 12th-13th century, the current saying is derived from a 16th-century line by William Shakespeare, 
<b><i>All that glisters is not gold</i></b>.
<br /> <br />
<b><i>All that glisters is not gold</i></b><br />
Often have you heard that told.<br />
Many a man his life hath sold<br />
But my outside to behold.<br />
Gilded tombs do worms enfold.<br />
Had you been as wise as bold,<br />
Young in limbs, in judgment old,<br />
Your answer had not been inscrolled<br />
Fare you well. Your suit is cold<br />

-William Shakespeare, Merchant of Venice, Act II Scene 7 
</p>

  <h4>Equation</h4>
  
    <i>x</i> = 1/3(<i>y</i><sub>1</sub><sup>2</sup> + <i>z</i><sub>1</sub><sup>2</sup>)

  <h4>Unordered Fruit List</h4>
  
    <ul>
      <li>Banana</li>
      <li>Mango</li>
      <li>Grapes</li>
      <li>Apples</li>
    </ul>
    
  <h4>Ordered Flower List</h4>
    <ol>
      <li>Jasmine</li>
      <li>Rose</li>
      <li>Lotus</li>
      <li>Tulip</li>
    </ol>
  <br />
</body>
</html>"""
   print(a)
   pc.copy(a)


def print_h2():
      a=r"""<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.1//EN" "http://www.w3.org/TR/xhtml11/DTD/xhtml11.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="en">
<head>
<title>Table Demo XHTML PAGE</title>
<meta name="author" content="Putta" />
<meta name="date" content="2023-02-17T04:58:37+0530" />
<meta http-equiv="content-type" content="text/html; charset=UTF-8"/>
<meta http-equiv="content-type" content="application/xhtml+xml; charset=UTF-8"/>
<meta http-equiv="content-style-type" content="text/css"/>
<meta http-equiv="expires" content="0"/>

<style>
table, th, td {
  border: 1px solid black;
  border-collapse: collapse;
}
th, td{
	padding-left: 10px;
	padding-bottom: 20px
}
table {
  border-spacing: 30px;
}
</style>

</head>
<body>

<h3>Tables in XHTML</h3>

<table align="center" width="70%" style="height:450px">
  <tr >
    <td rowspan="9" align="center" bgcolor=DEEEEE>
    	<b>Department</b>
    </td> 
    <td rowspan="3" align="center" bgcolor=9E7BA0>
	    <b>Sem1</b>
    </td>
    <td padding:15px>
    	<em>SubjectA</em>
    </td>    
  </tr>
  <tr>
    <td ><em>SubjectB</em></td>
  </tr>
  <tr>
    <td ><em>SubjectC</em></td>
  </tr>

  <tr>
    <td rowspan="3" align="center" bgcolor=9E7BA0>
	    <b>Sem2</b>
    </td>
    <td ><em>SubjectE</em></td>       
  </tr>
  <tr>
    <td ><em>SubjectF</em></td>
  </tr>
  <tr>
    <td ><em>SubjectG</em></td>
  </tr>

  <tr>
    <td rowspan="3" align="center" bgcolor=9E7BA0>
	    <b>Sem3</b>
    </td>
    <td ><em>SubjectH</em></td>       
  </tr>
  <tr>
    <td ><em>SubjectI</em></td>
  </tr>
  <tr>
    <td ><em>SubjectJ</em></td>
  </tr>

</table>

</body>
</html>"""
      print(a)
      pc.copy(a)



def print_h3():
   a=r"""<!DOCTYPE html>
<html>
<head>
	<meta charset="utf-8" />
	<title>HTML5 Demo</title>
	<meta http-equiv="refresh" content="5; URL=http://www.vtu.ac.in">
</head>
<body>
	<h3>HTML5 SVG</h3>
	<svg width="200" height="200" align="centre">
	  <rect x="50" y="50" width="100" height="100" fill="green" stroke="brown" stroke-width="6px"/>
	</svg>

	<h3>HTML5 MathML</h3>

	<math xmlns = "http://www.w3.org/1998/Math/MathML">
		     <mrow>
		        <msup><mi>d</mi></msup>            
		        <mo> = </mo>            
		        <msup><mi>x</mi><mn>2</mn></msup>
		        <mo>-</mo>				
		        <msup><mi>y</mi><mn>2</mn></msup>
		     </mrow>
	</math>

	<h3>This page redirects in 5 seconds</h3>
</body>
</html>"""
   print(a)
   pc.copy(a)


def print_h4():
   a=r"""<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8" />
<title>HTML5 Semantic Tags Demo</title>

      <style>
      body{
      background-color: #FFFDD0;
      }
      aside {
        float: right;
        width: 25%;
        background-color: cyan;
        font-style: italic;
        padding: 15px;
      }
      main {
        float: left;
        width: 70%;
      }
      footer {
        position: fixed;
        left: 0;
        bottom: 0;
        width: 100%;
        text-align: center;
      }
      mark { 
  background-color: yellow;
  color: black;
}
	figure {
  display: inline-block;
  margin: auto;
}

figcaption {
  font-style: italic;
}
    </style>

</head>
<body>
<article>
	<header>
    <h1>My Travelogue</h1>
    <p>Random Escapades</p>
  	</header>


<main>
    <figure>
    <img src="journey.jpeg" alt="Example Image" width="350" height="235">
    <figcaption>The road never ends</figcaption>
  </figure>

<section>
<h2>Ooty</h2>
<p>Ooty is a popular hill station located in the Nilgiri Hills. It is popularly called the "Queen of Hill Stations".</p>
</section>

<section>
<h2>Mysore</h2>
<p> The city is also known as the City of Palaces, Mysuru has always enchanted its visitors with its quaint charm.</p>
</section>

</main>

<aside>
<section>
<p>Upcoming Trek planned to <mark>Kumara Parvata</mark> will be sharing detils soon</p>
<details>
  <summary>Tentative Dates</summary>
  <p>24th January 2023</p>
</details>
</section>
</aside>

    <footer>
      <p>© 2023 Prabodh C P</p>
    </footer>

</article>
</body>
</html>"""
   print(a)
   pc.copy(a)



def print_h5():
   a=r"""<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8" />
<title>Class Selectors Demo</title>
<style>
.income {background-color: #0ff; font-style: italic;}
.expenses {background-color: #f0f;font-style: oblique;}
.profit {background-color: #ff0;font-weight: bold;}
.red{color: red;font-size: 24px;}
.strike{text-decoration: line-through; font-size: 24px;}
p {font-family: Cursive;}
</style>
</head>
<body>
<h1>Class Selectors Demo</h1>
<p>
Income, expenses, and profit are financial terms that are used to measure the financial health of a person or a business.
</p>
<p class="income">
Income refers to the amount of money received by an individual or business from various sources such as employment, investments, or sales of goods and services. Income can be earned on a regular basis, such as a salary, or irregularly, such as a bonus or one-time payment.
</p>

<p class="expenses">
Expenses, on the other hand, refer to the amount of money spent by an individual or business to cover their costs of living or operating. Expenses can include fixed costs such as rent or salaries, variable costs such as the cost of materials, or discretionary costs such as entertainment or travel.
</p>

<p class="profit">
Profit is the amount of money that remains after deducting expenses from income. It represents the financial gain or loss that a person or business has generated over a given period of time. A positive profit means that the income was greater than the expenses, while a negative profit means that the expenses were greater than the income.
</p>

<span class="strike">The current price is 50₹ </span><span class="red">and new price is 40₹</span>
 
</body>
</html>"""
   print(a)
   pc.copy(a)



def print_h6():
   a=r"""<!DOCTYPE html>
<html>
  <head>
  <meta charset="utf-8" />
  <title>Tag Properties </title>
  
    <style>
      .custom {
        display: inline;
        border: 2px double black;
        list-style-type: none;
        margin: 5px;
        padding-top: 10px;
        padding-right: 20px;
        padding-bottom: 10px;
        padding-left: 20px;
      }
      .logo {
    		list-style-image: url('https://www.w3schools.com/cssref/sqpurple.gif');
    		margin: 15px;
  	 }
    </style>
  </head>
  
  <body>
  <h2>li Tag Property modification Demo</h2>
  <h3>Current Top FootBall Players</h3>
  
    <ul>
      <li class="custom">Lionel Messi</li>
      <li class="custom">Kylian Mbappe</li>
      <li class="custom">Lewandowski</li>
    </ul>
  <br>
  <h2>list style type with user defined image logos</h2>
  <h3>Current Top FootBall Goalkeepers</h3>
    <ul class="logo">
      <li>Emiliano Martinez</li>
      <li>Thibaut Courtois</li>
      <li>Yassine Bounou</li>
    </ul>
  
  </body>
</html>"""
   print(a)
   pc.copy(a)



def print_h7():
   a=r"""<!DOCTYPE html>
<html>
<head>
	<title>Sign Up</title>
	<style>
		body {
			font-family: Arial, sans-serif;
			background-color: #f2f2f2;
		}

		.container {
			width: 500px;
			margin: 0 auto;
			padding: 20px;
			background-color: #F7E7CE;
			border-radius: 5px;
			box-shadow: 0 0 10px rgba(0,0,0,0.3);
		}

		table {
			width: 100%;
		}

		th, td {
			padding: 10px;
			
		}

		th {
			text-align: left;
			background-color: #f2f2f2;
		}

		input[type=text], input[type=password], input[type=email] {
			width: 100%;
			padding: 8px;
			margin: 8px 0;
			border: 1px solid #ccc;
			border-radius: 4px;
			box-sizing: border-box;
		}

		button[type=submit] {
			background-color: #FFA500;
			color: #fff;
			padding: 10px 20px;
			border: none;
			border-radius: 4px;
			cursor: pointer;
		}
	</style>
</head>
<body>
	<div class="container">
		<h1>Sign up Today</h1>
		<form>
			<table>
				<tr>
					<td><label for="username">Name:</label> <br> 
					<input type="text" id="username" name="username" required></td>
				</tr>

				<tr>
					<td><label for="email">Email:</label> <br> 
					<input type="email" id="email" name="email" required></td>
				</tr>

				<tr>
					<td><label for="password">Password:</label> <br> 
					<input type="password" id="password" name="password" required></td>
				</tr>
				<tr>
					<td><label for="password">Confirm password:</label> <br> 
					<input type="password" id="password" name="password" required></td>
				</tr>

				<tr>
					<td colspan="2"><button type="submit">Register</button></td>
				</tr>
			</table>
		</form>
	</div>
</body>
</html>"""
   print(a)
   pc.copy(a)



def print_h8():
   a=r"""<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8" />
<title></title>
<link rel="stylesheet" type="text/css" href="calcstyle.css">
</head>
<body>
<div class="calculator">
  <div class="display">
    <p id="result">0</p>
  </div>
  <div class="buttons">
    <button onclick="appendToDisplay('(')">(</button>
    <button onclick="appendToDisplay(')')">)</button>
    <button onclick="clearDisplay()">C</button>
    <button onclick="appendToDisplay('%')">%</button>    
    <button onclick="appendToDisplay('7')">7</button>
    <button onclick="appendToDisplay('8')">8</button>
    <button onclick="appendToDisplay('9')">9</button>
    <button onclick="appendToDisplay('*')">X</button>
    <button onclick="appendToDisplay('4')">4</button>
    <button onclick="appendToDisplay('5')">5</button>
    <button onclick="appendToDisplay('6')">6</button>
    <button onclick="appendToDisplay('-')">-</button>
    <button onclick="appendToDisplay('1')">1</button>
    <button onclick="appendToDisplay('2')">2</button>
    <button onclick="appendToDisplay('3')">3</button>
    <button onclick="appendToDisplay('+')">+</button>
    <button onclick="appendToDisplay('0')">0</button>
    <button onclick="appendToDisplay('.')">.</button>
    <button onclick="appendToDisplay('/')">/</button>
    <button onclick="evaluate()">=</button>
  </div>
</div>

</body>
</html>"""
   print(a)
   pc.copy(a)



def print_css8():
   a=r""".calculator {
  display: flex;
  flex-direction: column;
  width: 350px;
  margin: 10px;
  border: 1px solid #ccc;
  border-radius: 15px;
  background-color: #F0C0FF;
}

.display {

  background-color: #fff;
  border-radius: 10px;
  box-shadow: 0px 2px 5px rgba(0, 0, 0, 0.3);
  display: flex;
  justify-content: flex-end;
  align-items: center;
  padding: 10px;
  margin-left: 30px;
  margin-right: 30px;
  margin-top: 30px;
}

.buttons {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  padding: 20px;
}

button {
  padding: 20px;
  background-color: #8D918D;
  border: 1px solid #ccc;
  border-radius: 10px;
  cursor: pointer;
  margin: 10px;
  font-size: 18px;
  font-weight: bold;
}

button:hover {
  background-color: #d9d9d9;
}

button:active {
  background-color: #bfbfbf;
}

#result {
  margin: 0;
  font-size: 24px;
  font-weight: bold;
}"""
   print(a)
   pc.copy(a)



def print_h9():
   a=r"""<!DOCTYPE html>
<html>
  <head>
    <title>Scrolling Text Example</title>
    <style>
      #scrollingText {
        font-size: 24px; font-weight: bold; 
        white-space: nowrap; overflow: hidden;
      }
    </style>
  </head>
  <body>
    <button id="startBtn">Start Scrolling</button>
    <div id="scrollingText">This is some scrolling text!</div>
    <script>
      var scrollingText = document.getElementById("scrollingText");
      var startBtn = document.getElementById("startBtn");
      var textWidth = scrollingText.clientWidth;
      var containerWidth = scrollingText.parentNode.clientWidth;
      var currentPosition = 0;
      function scrollText() {
        if (currentPosition < containerWidth) {
          scrollingText.style.transform = "translateX(-" + currentPosition + "px)";
          currentPosition += 1;
          setTimeout(scrollText, 20);
        } else {
          currentPosition = -textWidth;
          scrollText();
        }
      }
      startBtn.addEventListener("click", function() {
        currentPosition = 0;
        scrollText();
      });
    </script>
  </body>
</html>"""
   print(a)
   pc.copy(a)



def print_h10():
   a=r"""<!DOCTYPE html>
<html lang="en">
	<head>
		<meta charset="utf-8">
		<meta name="author" content="Putta" >
		<title>Animal Stacking</title>
		<style>
		h1 {text-align: center;}

		.dog {
		position: absolute;
		left: 10%; top: 10%;
		z-index: 0;
		}
		.cat {
		position: absolute;
		left: 30%; top: 30%;
		z-index: 1;
		}
		.horse {
		position: absolute;
		left: 50%; top: 50%;
		z-index: 2;
		}
		</style>
		<script>
		var topIndex = 2;
		function moveToTop(picture) {
		picture.style.zIndex = ++topIndex;
		}

		</script>
	</head>
	<body>
		<h1>Image Overlap Demo</h1>
		<div id="image-container">
			<img id="dog" class="dog" src="dog.jpg" onmouseover="moveToTop(this)" width="400" height="300">
			<img id="cat" class="cat" src="cat.jpg" onmouseover="moveToTop(this)" width="400" height="300">
			<img id="horse" class="horse" src="horse.jpg" onmouseover="moveToTop(this)" width="400" height="300">
		</div>
	</body>
</html>"""
   print(a)
   pc.copy(a)
   

