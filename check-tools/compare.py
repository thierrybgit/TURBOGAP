import os
import sys

f_ref,f_run=open('../REF/Tests/trajectory_out.xyz','r'),open('Tests/trajectory_out.xyz','r')
xref,xrun=f_ref.readlines(),f_run.readlines()
f_ref.close()
f_run.close()

nitem,nitem_run=int(xref[0]),int(xrun[0])
if (nitem != nitem_run) :
    print("Pb taille fichier ref = ",nitem," run = ",nitem_run)
    sys.exit()
num,dem=0.,0.
for i in range(2,nitem):
    data_ref,data_run=xref[i].split()[1:],xrun[i].split()[1:]
    lref,lrun=len(data_ref),len(data_run)
    if (lref != lrun) :
        print("Pb taille line ref = ",lref," run = ",lrun)
        sys.exit()
    else:
        for n in range(lref):
            if (not("*" in data_run[n])):
                num +=pow(float(data_ref[n])-float(data_run[n]),2)
                dem +=pow(float(data_ref[n]),2)
print("======================================================")
if (dem==0.) :
    print(" Error on trajectory_out.xyz = ",pow(num,0.5))
else:
    print(" Error on trajectory_out.xyz = ",pow(num/dem,0.5))
print("======================================================\n")

liste,lfile,times=os.listdir('Tests'),[],0
for item in liste:
    if ("slurm-" in item): lfile.append(item)
for ind in range (len(lfile)):
    tmp = os.stat("Tests/"+lfile[ind])
    if (tmp.st_mtime >= times):
        times=tmp.st_mtime
        item=lfile[ind]
f_ref,f_run=open('../REF/Tests/run.out','r'),open('Tests/'+item,'r')
xref,xrun=f_ref.readlines(),f_run.readlines()
f_ref.close()
f_run.close()

data_e,data_t={"keys":[],"ref":[],"run":[]},{"keys":[],"ref":[],"run":[]}
for item in xref:
    if ("eV" in item):
        data_e["keys"].append(item.split(':')[0])
        data_e["ref"].append(float(item.split(':')[1].split()[0]))
    elif ("seconds" in item):
        x=item.split("seconds")[0]
        if ('*' in x) : x=x.split('*')[1]
        if ('-' in x) : x="    "+x.split('-')[1]
        x=x.split(':')
        data_t["keys"].append(x[0])
        data_t["ref"].append(float(x[1].split()[0]))
for item in xrun:
    if ("eV" in item):
        data_e["run"].append(float(item.split(':')[1].split()[0]))
    elif ("seconds" in item):
        x=item.split("seconds")[0]
        if ('*' in x) : x=x.split('*')[1]
        if ('-' in x) : x="    "+x.split('-')[1]
        x=x.split(':')
        data_t["run"].append(float(x[1].split()[0]))

print("Comparison for energy\n diff\t\tkeys\t\tref\t\t\trun")
print("====================================================================\n")
for i in range(len(data_e["keys"])):
    x1,x2=data_e["ref"][i],data_e["run"][i]
    print(" ",abs(x1-x2),'\t',data_e["keys"][i],'\t',x1,'\t',x2)

print("====================================================================\n")
print("Time comparison\n \tkeys\t\tref\trun\tgain ")
print("=============================================\n")
for i in range(len(data_t["keys"])):
    x1,x2,x3=data_t["ref"][i],data_t["run"][i],data_t["ref"][i]
    if (x2!=0.) : x3=((x1/x2)-1)*100
    print('{0:13}'.format(data_t["keys"][i])," {0:11.3f}".format(x1),'{0:7.3f}'.format(x2),"{0:7.2f}".format(x3))
print("=============================================\n")
