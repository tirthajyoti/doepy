# DOEPY (`pip install doepy`)
---
![doe-1](https://raw.githubusercontent.com/tirthajyoti/doepy/master/images/doe_1.PNG)
#### Authored and maiantained by Dr. Tirthajyoti Sarkar, Fremont, CA 94536 (https://tirthajyoti.github.io)

## Introduction
[Design of Experiment (DOE)](https://en.wikipedia.org/wiki/Design_of_experiments) is an important activity for any scientist, engineer, or statistician planning to conduct experimental analysis. This exercise has become **critical in this age of rapidly expanding field of data science and associated statistical modeling and machine learning**. A well-planned DOE can give a researcher meaningful data set to act upon with optimal number of experiments preserving critical resources.

> After all, aim of Data Science is essentially to conduct highest quality scientific investigation and modeling with real world data. And to do good science with data, one needs to collect it through carefully thought-out experiment to cover all corner cases and reduce any possible bias.

### What is a scientific experiment?
In its simplest form, a scientific experiment aims at predicting the outcome by introducing a change of the preconditions, which is represented by one or more [independent variables](https://en.wikipedia.org/wiki/Dependent_and_independent_variables), also referred to as “input variables” or “predictor variables.” The change in one or more independent variables is generally hypothesized to result in a change in one or more [dependent variables](https://en.wikipedia.org/wiki/Dependent_and_independent_variables), also referred to as “output variables” or “response variables.” The experimental design may also identify [control variables](https://en.wikipedia.org/wiki/Controlling_for_a_variable) that must be held constant to prevent external factors from affecting the results.

### What is Experimental Design?
Experimental design involves not only the selection of suitable independent, dependent, and control variables, but planning the delivery of the experiment under statistically optimal conditions given the constraints of available resources. There are multiple approaches for determining the set of design points (unique combinations of the settings of the independent variables) to be used in the experiment.

Main concerns in experimental design include the establishment of [validity](https://en.wikipedia.org/wiki/Validity_%28statistics%29), [reliability](https://en.wikipedia.org/wiki/Reliability_%28statistics%29), and [replicability](https://en.wikipedia.org/wiki/Reproducibility). For example, these concerns can be partially addressed by carefully choosing the independent variable, reducing the risk of measurement error, and ensuring that the documentation of the method is sufficiently detailed. Related concerns include achieving appropriate levels of [statistical power](https://en.wikipedia.org/wiki/Statistical_power) and [sensitivity](https://en.wikipedia.org/wiki/Sensitivity_and_specificity).

Need for careful design of experiment arises in all fields of serious scientific, technological, and even social science investigation — *computer science, physics, geology, political science, electrical engineering, psychology, business marketing analysis, financial analytics*, etc…

### Options for open-source DOE builder package in Python?
Unfortunately, majority of the state-of-the-art DOE generators are part of commercial statistical software packages like [JMP (SAS)](https://www.jmp.com/) or [Minitab](www.minitab.com/en-US/default.aspx). However, a researcher will surely be benefited if there exists an open-source code which presents an intuitive user interface for generating an experimental design plan from a simple list of input variables. There are a couple of DOE builder Python packages but individually they don’t cover all the necessary DOE methods and they lack a simplified user API, where one can just input a CSV file of input variables’ range and get back the DOE matrix in another CSV file.

---

## Features
This set of codes is a collection of functions which wrap around the core packages (mentioned below) and generate **design-of-experiment (DOE) matrices** for a statistician or engineer from an arbitrary range of input variables.

### Limitation of the foundation packages used
Both the core packages, which act as foundations to this repo, are not complete in the sense that they do not cover all the necessary functions to generate DOE table that a design engineer may need while planning an experiment. Also, they offer only low-level APIs in the sense that the standard output from them are normalized numpy arrays. It was felt that users, who may not be comfortable in dealing with Python objects directly, should be able to take advantage of their functionalities through a simplified user interface.

### Simplified user interface
***User just needs to provide a simple CSV file with a single table of variables and their ranges (2-level i.e. min/max or 3-level).*** Some of the functions work with 2-level min/max range while some others need 3-level ranges from the user (low-mid-high). Intelligence is built into the code to handle the case if the range input is not appropriate and to generate levels by simple linear interpolation from the given input. The code will generate the DOE as per user's choice and write the matrix in a CSV file on to the disk. 

In this way, ***the only API user needs to be exposed to, are input and output CSV files. These files then can be used in any engineering simulator, software, process-control module, or fed into process equipments.***

### Designs available
* Full factorial,
* 2-level fractional factorial,
* Plackett-Burman,
* Sukharev grid,
* Box-Behnken,
* Box-Wilson (Central-composite) with center-faced option,
* Box-Wilson (Central-composite) with center-inscribed option,
* Box-Wilson (Central-composite) with center-circumscribed option,
* Latin hypercube (simple),
* Latin hypercube (space-filling),
* Random k-means cluster,
* Maximin reconstruction,
* Halton sequence based,
* Uniform random matrix

---

## How to use it?
### What supporitng packages are required?
First make sure you have all the necessary packages installed. You can simply run the .bash (Unix/Linux) and .bat (Windows) files provided in the repo, to install those packages from your command line interface. They contain the following commands,

```
pip install numpy
pip install pandas
pip install pydoe
pip install diversipy
```

### How to install the package?
You can pip install the package!

```pip install doepy```

### Quick start
Let's say you have a design problem with the following table for the parameters range. Imagine this as a generic example of a checmical process in a manufacturing plant. You have 3 levels of `Pressure`, 3 levels of `Temperature`, 2 levels of `FlowRate`, and 2 levels of `Time`.

`Pressure`: 40/55/70<br>
`Temperature`: 290/320/350<br>
`FlowRate`: 0.2/0.4<br>
`Time`: 5/8

First, import `build` module from the package,

```from doepy import build```

Then, try a simple example by building a **full factorial design**.
<br> We will use `build.full_fact()` function for this.
<br>You have to pass a dictionary object to the function which encodes your experimental data.

```build.full_fact({'Pressure':[40,55,70],'Temperature':[290, 320, 350],'Flow rate':[0.2,0.4], 'Time':[5,8]})```

If you build a full-factorial DOE out of this, you should get a table with 3x3x2x2 = 36 entries.

### Other functions to try on

Try other functions like `build.space_filling_lhs()` to construct a [space-filling Latin hypercube design](https://en.wikipedia.org/wiki/Latin_hypercube_sampling).

Or try one of the center-composite designs.

Many more to be added!

### Read from and write to CSV files

Internally, you pass on a dictionary object and get back a Pandas DataFrame. But, for reading from and writing to CSV files, you have to use the `read_write` module of the package.

```
from doepy import read_write
data_in=read_write.read_variables_csv('../Data/params.csv')
```

Then you can use this `data_in` object in the DOE generating functions.

For writing back to a CSV,

```
df_lhs=build.space_filling_lhs(data_in,num_samples=100)
filename = 'lhs'
read_write.write_csv(df_lhs,filename=filename)
```

You should see a `lhs.csv` file in your directory.

---

## Acknowledgements and Requirements
The code was written in Python 3.7. It uses following external packages that needs to be installed on your system to use it,
* pydoe: A package designed to help the scientist, engineer, statistician, etc., to construct appropriate experimental designs. [Check the docs here](https://pythonhosted.org/pyDOE/).
* diversipy: A collection of algorithms for sampling in hypercubes, selecting diverse subsets, and measuring diversity. [Check the docs here](https://www.simonwessing.de/diversipy/doc/).
* numpy
* pandas