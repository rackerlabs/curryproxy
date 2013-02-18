using System;
using System.Collections.Generic;
using System.Linq;
using System.Web;
using System.Web.Mvc;
using System.Web.Routing;

namespace Curry.Services
{
    public class RouteConfig
    {
        public static void RegisterRoutes(RouteCollection routes)
        {
            routes.IgnoreRoute("{resource}.axd/{*pathInfo}");

            //we could have used just used rewriting rule to redirect request instead of all this Jazz, if we dont have to cache the response

            routes.MapRoute("CurryProxyDev", "dev/{*path}", new { controller = "CurryRouter", action = "RedirectToDevUrl" });
            routes.MapRoute("CurryProxyTest", "test/{*path}", new { controller = "CurryRouter", action = "RedirectToTestUrl" });
            routes.MapRoute("CurryProxyQA", "qa/{*path}", new { controller = "CurryRouter", action = "RedirectToQAUrl" });
            routes.MapRoute("CurryProxyPP", "preprod/{*path}", new { controller = "CurryRouter", action = "RedirectToPreProdUrl" });
            routes.MapRoute("CurryProxyProd", "prod/{*path}", new { controller = "CurryRouter", action = "RedirectToprodUrl" });
            routes.MapRoute("CurryProxyMany", "{[0-9a-zA-Z]+(,[0-9a-zA-Z]+)}/{*path}", new { controller = "CurryRouter", action = "MixItUp" });
            

        }
    }
}