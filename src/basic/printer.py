#-----------------------------------------------------------------------------------------------------
# printer.py
#-----------------------------------------------------------------------------------------------------
import datetime
#-----------------------------------------------------------------------------------------------------

#=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
# Printing functions
#=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
def strA(arr, start="[\n\t", sep="\n\t", end="\n]"):
    """ returns a string representation of an array/list for printing """
    res=start
    for a in arr:
        res += (str(a) + sep)
    return res + end
#=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
def strD(arr, sep="\n", cep="\t:\t", caption=""):
    """ returns a string representation of a dict object for printing """
    res="=-=-=-=-==-=-=-=-="+sep+"DICT: "+caption+sep+"=-=-=-=-==-=-=-=-="+sep
    for i in arr:
        res+=str(i) + cep + str(arr[i]) + sep
    return res + "=-=-=-=-==-=-=-=-="+sep
#=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
def show(x, P = print):
    """ prints x.__dict__ using strD() """
    P(strD(x.__dict__, cep='\t\t:', caption=str(x.__class__)))
#=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
def shows(*X, P = print):
    """ prints x.__dict__ using strD() """
    for x in X:
        show(x, P)
#=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
def showx(x, P = print, sw='_'):
    for d in dir(x):
        if not d.startswith(sw):
            v = ""
            try:
                v = getattr(x, d)
            except:
                v='?'
            P(d, '\t\t:', v)
#=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
 

#=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
# Time-stamping functions
#=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
def now(format='%Y-%m-%d %H:%M:%S::%f'):
    """ formated time stamp 
        %a	Weekday, short version	Wed	
        %A	Weekday, full version	Wednesday	
        %w	Weekday as a number 0-6, 0 is Sunday	3	
        %d	Day of month 01-31	31	
        %b	Month name, short version	Dec	
        %B	Month name, full version	December	
        %m	Month as a number 01-12	12	
        %y	Year, short version, without century	18	
        %Y	Year, full version	2018	
        %H	Hour 00-23	17	
        %I	Hour 00-12	05	
        %p	AM/PM	PM	
        %M	Minute 00-59	41	
        %S	Second 00-59	08	
        %f	Microsecond 000000-999999	548513	
        %z	UTC offset	+0100	
        %Z	Timezone	CST	
        %j	Day number of year 001-366	365	
        %U	Week number of year, Sunday as the first day of week, 00-53	52	
        %W	Week number of year, Monday as the first day of week, 00-53	52	
        %c	Local version of date and time	Mon Dec 31 17:41:00 2018	
        %C	Century	20	
        %x	Local version of date	12/31/18	
        %X	Local version of time	17:41:00	
        %%	A % character	%	
        %G	ISO 8601 year	2018	
        %u	ISO 8601 weekday (1-7)	1	
        %V	ISO 8601 weeknumber (01-53)	01
    """
    return datetime.datetime.strftime(datetime.datetime.now(), format)
#=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
def strU(sep=''):
    """ formated time stamp based UID """
    return datetime.datetime.strftime(datetime.datetime.now(), sep.join("%Y","%m","%d","%H","%M","%S","%f"))
#=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
def strUx(start='', sep='', end=''):
    """ xtended formated time stamp based UID """
    return start + datetime.datetime.strftime(datetime.datetime.now(), sep.join("%Y","%m","%d","%H","%M","%S","%f")) + end


#-----------------------------------------------------------------------------------------------------
# Foot-Note:
""" NOTE:
    * Author:           Nelson.S
"""
#-----------------------------------------------------------------------------------------------------
