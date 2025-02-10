using Python.Runtime;
using System;
using System.IO;
using System.Reflection;

class Program
{
    static void Main()
    {
        Console.WriteLine("Hello, World! From C#");

        string scriptName = "pythonfile.py";
        string scriptName2 = "powershelltest.py";
        //string scriptPath = ExtractEmbeddedResource(scriptName);
        //string pythonPackagePath = ExtractEmbeddedPythonPackage("python-3.12.8-embed-amd64");
        string pythonPackagePath = "python3";
        RunScript(scriptName, scriptName2, pythonPackagePath);
        
    }

    static void RunScript(string scriptPath, string scriptPath2, string pythonPackagePath)
    {
        string pythonDllPath = Path.Combine(AppDomain.CurrentDomain.BaseDirectory, @$"{pythonPackagePath}\python312.dll");
        if (!File.Exists(pythonDllPath))
        {
            throw new FileNotFoundException($"The file {pythonDllPath} does not exist.");
        }

        Runtime.PythonDLL = pythonDllPath;
        PythonEngine.Initialize();
        using (Py.GIL())
        {
            dynamic pythonScript = Py.Import(Path.GetFileNameWithoutExtension(scriptPath));
            dynamic pythonScript2 = Py.Import(Path.GetFileNameWithoutExtension(scriptPath2));
            //dynamic result = pythonScript.hello_world();
            //Console.WriteLine(result);
        }
    }

}


