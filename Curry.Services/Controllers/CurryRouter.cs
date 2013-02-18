using System;
using System.Collections.Generic;
using System.Linq;
using System.Web;
using System.Web.Mvc;
using Curry.Services.Results;
using System.Threading.Tasks;
using System.Collections;


namespace Curry.Services
{

    public class CurryRouterController : AsyncController
    {
        public delegate object ComputeDelegate(string env, Uri originalUrl, HttpRequestBase currentReq);

        CurryConfiguration config = new CurryConfiguration();
        
        CurryManager curryManager = new CurryManager();

      

        public ActionResult RedirectToDevUrl()
        {  

            return ForwardRequest(CurryConfigKeys.DEV);
        }


        public ActionResult RedirectToTestUrl()
        {

            return ForwardRequest(CurryConfigKeys.TEST);
        }


        public ActionResult RedirectToQAUrl()
        {

            return ForwardRequest(CurryConfigKeys.QA);
        }



        public ActionResult RedirectToPreProdUrl()
        {
           
            return ForwardRequest(CurryConfigKeys.PREPROD);
        }

       


        public ActionResult RedirectToprodUrl()
        {
            return ForwardRequest(CurryConfigKeys.PROD);
            
        }

        private ActionResult ForwardRequest(CurryConfigKeys env)
        {
            ActionResult result;

            CurryRelayResponse response = curryManager.RelayRequest(env.ToString().ToLowerInvariant(), HttpContext.Request.Url, this.Request);
            HttpContext.Response.StatusCode = (int)response.httpStatusCode;
            result = new ObjectResult(response.data);


            return result;
        }

        //Still Under Development - doesnt work yet
        public ActionResult MixItUp()
        {

            string[] environments = HttpContext.Request.Url.Segments[1].Replace("/", string.Empty).Split(',');
            string originalCommaDelimitedEnvs = HttpContext.Request.Url.Segments[1];

            List<string> sanitizedOriginalUri = new List<string>();

            foreach (string env in environments)
            {
                sanitizedOriginalUri.Add(HttpContext.Request.Url.OriginalString.Replace(originalCommaDelimitedEnvs,(env+"/")));
            }

            List<ComputeDelegate> delegates = new List<ComputeDelegate>();



            foreach (string origUri in sanitizedOriginalUri)
            {
                delegates.Add(new ComputeDelegate(curryManager.RelayRequest));
               
            }


            Task<CurryRelayResponse>[] tasks = new Task<CurryRelayResponse>[]
            {
                Task<CurryRelayResponse>.Factory.StartNew(() => curryManager.RelayRequest("dev", new Uri("http://curry.drivesrvr.com/dev/v1.0/user/agents"), this.Request)),
                Task<CurryRelayResponse>.Factory.StartNew(() => curryManager.RelayRequest("test", new Uri("http://curry.drivesrvr.com/test/v1.0/user/agents"), this.Request)),
                Task<CurryRelayResponse>.Factory.StartNew(() => curryManager.RelayRequest("prod", new Uri("http://curry.drivesrvr.com/prod/v1.0/user/agents"), this.Request))
            };

            //Block until all tasks complete.
            Task.WaitAll(tasks);
            
            IEnumerable resultList0 = tasks[0].Result.data as IEnumerable;
            IEnumerable resultList1 = tasks[1].Result.data as IEnumerable;
            IEnumerable resultList2 = tasks[2].Result.data as IEnumerable;

            List<object> List0 = resultList0.Cast<object>().ToList();
            List<object> List1 = resultList1.Cast<object>().ToList();
            List<object> List2 = resultList2.Cast<object>().ToList();

            List<object> aggregatedList = List0.Concat(List1).Concat(List2).ToList(); 


            return new ObjectResult(aggregatedList);

        }


      
  
    }
}
