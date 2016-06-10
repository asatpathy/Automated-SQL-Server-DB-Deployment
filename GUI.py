from tkinter import *
from tkinter.ttk import *
import subprocess

class Application(Frame):

    def __init__(self, master):
        Frame.__init__(self,master)
        self.grid()
        self.create_widgets()

    def create_widgets(self):
        #Declare variables ######################################################
        self.SourceServerString=StringVar()
        self.SourceDatabaseString=StringVar()

        self.TargetServerString=StringVar()
        self.TargetDatabaseString=StringVar()

        self.InformationString=StringVar()

        self.PreDeploymentQueryString=StringVar()

        self.ShellOutputPreDeploymentString=StringVar()
        self.ShellOutputExtractString=StringVar()
        self.ShellOutputPublishString=StringVar()

        self.WinAuthSrcVariable=BooleanVar()
        self.WinAuthSrcVariable.set(True)

        self.WinAuthTrgtVariable=BooleanVar()
        self.WinAuthTrgtVariable.set(True)


        #Create widgets ##########################################################
        #Label and Text Area for Pre-Deployment Script
        self.PreDeploymentLabel=Label(self,text="Enter Pre-deployment script")
        self.PreDeploymentLabel.grid(row=0,column=0,sticky=W)

        self.PreDeploymentText=Text(self, width=40, height=5, wrap=WORD)
        self.PreDeploymentText.grid(row=0, column=1, columnspan=2, sticky=W)

        #Label and Textbox for Source Connection
        self.SourceServerLabel=Label(self, text="Source Server")
        self.SourceServerLabel.grid(row=1,column=0,sticky=W)
        self.SourceServerEntry=Entry(self)
        self.SourceServerEntry.grid(row=1,column=1,sticky=W)

        self.SourceDatabaseLabel=Label(self, text="Source Database")
        self.SourceDatabaseLabel.grid(row=2,column=0,sticky=W)
        self.SourceDatabaseEntry=Entry(self)
        self.SourceDatabaseEntry.grid(row=2,column=1,sticky=W)

        # Label and Textbox for Target Connection
        self.TargetServerLabel=Label(self, text="Target Server")
        self.TargetServerLabel.grid(row=1,column=2,sticky=W)
        self.TargetServerEntry=Entry(self)
        self.TargetServerEntry.grid(row=1,column=3,sticky=W)
        self.TargetServerEntry.insert(0,"localhost")

        self.TargetDatabaseLabel=Label(self, text="Target Database")
        self.TargetDatabaseLabel.grid(row=2,column=2,sticky=W)
        self.TargetDatabaseEntry=Entry(self)
        self.TargetDatabaseEntry.grid(row=2,column=3,sticky=W)

        #Windows Authentication checkboxes
        self.WinAuthSrcCheckButton=Checkbutton(self,text="Source Windows Auth", var=self.WinAuthSrcVariable, command=self.SrcCredentials_Visibility)
        self.WinAuthSrcCheckButton.grid(row=3,column=0,sticky=W)

        self.WinAuthTrgtCheckButton=Checkbutton(self,text="Target Windows Auth", var=self.WinAuthTrgtVariable, command=self.TrgtCredentials_Visibility)
        self.WinAuthTrgtCheckButton.grid(row=3,column=2,sticky=W)

        #Label and Textbox for Source Credentials
        self.SourceUsernameLabel=Label(self, text="Source Username")
        self.SourceUsernameEntry=Entry(self)
        self.SourcePasswordLabel=Label(self, text="Source Password")
        self.SourcePasswordEntry=Entry(self, show="*")

        # Label and Textbox for Target Credentials
        self.TargetUsernameLabel=Label(self, text="Target Username")
        self.TargetUsernameEntry=Entry(self)
        self.TargetPasswordLabel=Label(self, text="Target Password")
        self.TargetPasswordEntry=Entry(self, show="*")

        #Button for initiating the deployment
        self.ExecuteButton=Button(self,text="Compare & Deploy",command=self.execute_all)  #button click calls execute_all method
        self.ExecuteButton.grid(row=10,column=1,sticky=W)

        #Button to check Shell Output
        self.ExecuteButton=Button(self,text="Shell Output",command=self.shell_output)  #button click calls shell output
        self.ExecuteButton.grid(row=10,column=2,sticky=W)

        #Connection information
        self.InformationLabel=Label(self,text="Connection Info:",justify=LEFT)
        self.InformationLabel.grid(row=11,column=0,sticky=W)



    #Methods######################################################################
    #method that initiates the process to compare & deploy SQL Server database
    def execute_all(self):
        self.SourceServerString=self.SourceServerEntry.get()
        self.SourceDatabaseString=self.SourceDatabaseEntry.get()

        self.TargetServerString = self.TargetServerEntry.get()
        self.TargetDatabaseString=self.TargetDatabaseEntry.get()

        self.PreDeploymentQueryString=self.PreDeploymentText.get(1.0,END)

        # self.TargetServerEntry.delete(0, END)
        # self.TargetDatabaseEntry.delete(0, END)
        #
        # self.TargetServerEntry.insert(0,self.SourceServerString)
        # self.TargetDatabaseEntry.insert(0,self.SourceDatabaseString)

        # subprocess.call(
        #     'sqlcmd -S '+ self.SourceServerString +' -d '+ self.SourceDatabaseString +' -i CompareDeploy\\insertNewSQLPackage1.sql',shell=True)

        SPPreDeployment=subprocess.Popen('sqlcmd -S '+ self.TargetServerString +' -d master -Q " ' + self.PreDeploymentQueryString + ' "',stdout=subprocess.PIPE)
        SPExtract=subprocess.Popen('CompareDeploy\\sqlpackage /Action:Extract /SourceServerName:'+ self.SourceServerString +' /SourceDatabaseName:'+ self.SourceDatabaseString +' /TargetFile:CompareDeploy\\temp\\'+ self.SourceDatabaseString +'.dacpac',stdout=subprocess.PIPE)
        SPPublish=subprocess.Popen('CompareDeploy\\sqlpackage /Action:Publish /SourceFile:CompareDeploy\\temp\\'+ self.SourceDatabaseString +'.dacpac /TargetServerName:'+ self.TargetServerString +' /TargetDatabaseName:'+ self.TargetDatabaseString +' /p:ExcludeObjectTypes=RoleMembership;Users /p:ScriptDatabaseOptions=False /p:BlockOnPossibleDataLoss=False',stdout=subprocess.PIPE)

        self.ShellOutputPreDeploymentString=SPPreDeployment.communicate()[0]
        self.ShellOutputExtractString=SPExtract.communicate()[0]
        self.ShellOutputPublishString=SPPublish.communicate()[0]

        self.InformationString='Connection Info:\nSource Server: ' + self.SourceServerString + '\nSource Database: ' + self.SourceDatabaseString + '\nTarget Server: ' + self.TargetServerString + '\nTarget Database: ' + self.TargetDatabaseString
        self.InformationLabel["text"]=self.InformationString



    #method to display shell output
    def shell_output(self):
        # Shell output window
        ShellOutputWindow = Toplevel(width=500,height=700)
        ShellOutputWindow.title("Shell Output")
        ShellOutputWindow.grid()

        ShellOutputText=Text(ShellOutputWindow, width=100, height=40, wrap=WORD)
        ShellOutputText.grid(row=0, column=1, columnspan=2, sticky=W)
        ShellOutputText.insert(END, self.ShellOutputPreDeploymentString + self.ShellOutputExtractString + self.ShellOutputPublishString)



    def SrcCredentials_Visibility(self):
        if self.WinAuthSrcVariable.get() is True:
            self.SourceUsernameLabel.grid_remove()
            self.SourceUsernameEntry.grid_forget()
            self.SourcePasswordLabel.grid_forget()
            self.SourcePasswordEntry.grid_forget()

        else:
            self.SourceUsernameLabel.grid(row=4, column=0, sticky=W)
            self.SourceUsernameEntry.grid(row=4, column=1, sticky=W)
            self.SourcePasswordLabel.grid(row=5, column=0, sticky=W)
            self.SourcePasswordEntry.grid(row=5, column=1, sticky=W)



    def TrgtCredentials_Visibility(self):
        if self.WinAuthTrgtVariable.get() is True:
            self.TargetUsernameLabel.grid_forget()
            self.TargetUsernameEntry.grid_forget()
            self.TargetPasswordLabel.grid_forget()
            self.TargetPasswordEntry.grid_forget()

        else:
            self.TargetUsernameLabel.grid(row=4, column=2, sticky=W)
            self.TargetUsernameEntry.grid(row=4, column=3, sticky=W)
            self.TargetPasswordLabel.grid(row=5, column=2, sticky=W)
            self.TargetPasswordEntry.grid(row=5, column=3, sticky=W)

root=Tk()
root.title("Compare and Deploy SQL Server database")
root.geometry("800x450")
app=Application(root)
root.mainloop()