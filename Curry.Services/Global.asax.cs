using System;
using System.Collections.Generic;
using System.Linq;
using System.Web;
using System.Web.Http;
using System.Web.Mvc;
using System.Web.Optimization;
using System.Web.Routing;


namespace Curry.Services
{
    // Note: For instructions on enabling IIS6 or IIS7 classic mode, 
    // visit http://go.microsoft.com/?LinkId=9394801

    public class WebApiApplication : System.Web.HttpApplication
    {
        protected void Application_Start()
        {
            AreaRegistration.RegisterAllAreas();

          
            FilterConfig.RegisterGlobalFilters(GlobalFilters.Filters);
            RouteConfig.RegisterRoutes(RouteTable.Routes);
            BundleConfig.RegisterBundles(BundleTable.Bundles);
        }

        /// <report>
        /// Do this on all incoming requests
        /// </report>
        protected void Application_BeginRequest()
        {

           // // we need to pre authorize a request to this api when a reflighted request comes in (currently by Firefox and Chrome,...)
           // // see https://developer.mozilla.org/En/HTTP_access_control for details on this standard.
           //// HttpContext.Current.Response.AddHeader("Access-Control-Allow-Origin", AppSetting.Settings[WEBSITE_SETTING.ApprovedClient.ToString()]);
           // HttpContext.Current.Response.AddHeader("Access-Control-Allow-Credentials", "true");
           // HttpContext.Current.Response.AddHeader("Access-Control-Allow-Headers", "x-requested-with, content-type, x-auth-token, content-length, connection, accept");
           // HttpContext.Current.Response.AddHeader("Access-Control-Allow-Methods", "POST, GET, PUT, DELETE");//, OPTIONS");
           // HttpContext.Current.Response.AddHeader("Access-Control-Max-Age", "1728000");

           // if (HttpContext.Current.Request.HttpMethod == "OPTIONS")
           // {
           //     HttpContext.Current.Response.End();
           // }


           // HttpRequest request = HttpContext.Current.Request;
           

           // HttpContext.Current.Items.Add("RequestGUID", Guid.NewGuid().ToString());
        }

       
    }
}