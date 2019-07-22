from doepy import build, read_write
print("\nFull factorial")
print("-"*50)
build.full_fact({'Pressure':[50,60,70],'Temperature':[290, 320, 350],'Flow rate':[0.9,1.0]}).head()
print('Test passed')

print("\nReading an example csv")
print("-"*50)
d1=read_write.read_variables_csv('../Data/params.csv')
print('Test passed')

print("\nCC design")
print("-"*50)
build.central_composite(d1,center=(1,1))
print('Test passed')

print("\nPB design")
print("-"*50)
build.plackett_burman(d1)
print('Test passed')

print("\nBB design")
print("-"*50)
build.box_behnken(d1)
print('Test passed')

print("\nHalton")
print("-"*50)
build.halton(d1,num_samples=10)
print('Test passed')

print("\nk-means")
print("-"*50)
build.random_k_means(d1,num_samples=8)
print('Test passed')

print("\nUniform random")
print("-"*50)
build.uniform_random(d1,12)
print('Test passed')

print("\nLHS")
print("-"*50)
build.lhs(d1,num_samples=20,prob_distribution='Normal')
print('Test passed')

print("\nSpace filling LHS")
print("-"*50)
build.space_filling_lhs(d1,num_samples=100)
print('Test passed')

print("\nWriting to a CSV file")
print("-"*50)
df1=build.space_filling_lhs(d1,num_samples=100)
filename = 'df1.csv'
read_write.write_csv(df1,filename=filename)
print('Test passed')

# Cleanup the generated CSV
import os
os.remove(filename)

d2 = {'A':[1,5],'B':[0.3,0.7],'C':[10,15],'D':[3,7],'E':[-2,-1]}
print("\nFractional factorial")
print("-"*50)
build.frac_fact_res(d2)
print('Test passed')
