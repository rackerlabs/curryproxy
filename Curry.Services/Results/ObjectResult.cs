using System;
using System.Collections.Generic;
using System.Linq;
using System.Web;
using System.Web.Mvc;
using System.Xml.Serialization;
using System.Net;

namespace Curry.Services.Results
{
    /// <report>
    /// Allows returning  result in various formats.
    /// </report>
    public class ObjectResult : ActionResult
    {
        /// <summary>
        /// The Data to serialize and return
        /// </summary>
        public object Data { get; set; }

        public HttpStatusCode ResponseStatusCode { get; set; }

        /// <report>
        /// Initializes a new instance of the <see cref="ObjectResult"/> class.
        /// </report>
        /// <param name="data">The object to serialize.</param>
        public ObjectResult(object data)
        {
            this.ResponseStatusCode = HttpStatusCode.OK;
            this.Data = data;
        }


        public ObjectResult(object data, HttpStatusCode responseStatus)
        {
            this.Data = data;
            this.ResponseStatusCode = responseStatus;
        }
        

        /// <report>
        /// Gets the object to be serialized.
        /// </report>
        public object GetData
        {            
            get { return this.Data; }
        }

        

        /// <report>
        /// Serializes the object that was passed into the constructor and writes tp the result stream.
        /// </report>
        /// <param name="context">The controller context for the current request.</param>
        public override void ExecuteResult(ControllerContext context)
        {
            if (this.Data != null)
            {
                string format = context.RouteData.Values["format"] != null ? context.RouteData.Values["format"].ToString() : string.Empty;
                switch (format)
                {
                    case "xml":
                        context.HttpContext.Response.ContentType = "text/xml";
                        new XmlResult(this.Data).ExecuteResult(context);
                        break;


                    case "json":
                    default:
                        context.HttpContext.Response.ContentType = "application/json; charset=ISO-8859-1";
                        context.HttpContext.Response.StatusCode = (int)this.ResponseStatusCode;
                        LargeJsonResult result = new LargeJsonResult { Data = this.Data };
                        result.JsonRequestBehavior = JsonRequestBehavior.AllowGet;
                        result.ExecuteResult(context);
                        break;
                }
            }
        }
    }

}