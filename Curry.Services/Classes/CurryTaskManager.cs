
namespace Curry.Services
{
    /// <summary>
    /// Executes tasks asynchronously by calling into TPL
    /// </summary>
    public class CurryTaskManager
    {
        // http://stackoverflow.com/questions/6715005/best-way-to-call-two-web-services-from-method-without-blocking-each-other
        //http://codingndesign.com/blog/?p=195

        public static void RunTasks()
        {
            //Task[] tasks = new Task[3]
            //{
            //    Task.Factory.StartNew(() => MethodA()),
            //    Task.Factory.StartNew(() => MethodB()),
            //    Task.Factory.StartNew(() => MethodC())
            //};
        }
       

        public static T ExecuteTask<T>()
        {
            T taskResult = default(T);
            return taskResult;
        }
    }
}

