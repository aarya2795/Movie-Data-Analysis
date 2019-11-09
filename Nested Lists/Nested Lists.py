#!/usr/bin/env python
# coding: utf-8

# <h2> Nested Lists </h2>
# <h4><u> Problem Statment </u></h4>
# <br>
# Given the names and grades for each student in a Physics class of  students, store them in a nested list and print the name(s) of any student(s) having the second lowest grade.
# <br>
# <b>Note:</b> If there are multiple students with the same grade, order their names alphabetically and print each name on a new line.

# In[1]:


if __name__ == '__main__':
    student_data = []
    for _ in range(int(input())):
        name = input()
        score = float(input())
        student_data.append([name,score])
    
    # for each record in student_data
    # sort via the scores in ascending order
    # with '{}' within sorted[], creates a "set"
    # Note: here we are using set as it removes the additional same numbers
    sortedScores = sorted({s[1] for s in student_data})

    # for each record in student_data (s)
    # namesSorted is a soreted (by name which is s[0]) list of all students 
    # whose score is equal to the second lowest score which is s[1] in scoresSorted
    namesSorted = sorted(s[0] for s in student_data if (sortedScores[1]==s[1]))
    
    #.join(namesSorted) takes each element in the nameSort list
    # "\n" seperates using a newline BETWEEN each element
    print("The names having second lowest grade are: ")
    print('\n'.join(namesSorted))


# In[ ]:




