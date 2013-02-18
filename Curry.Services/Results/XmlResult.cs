using System;
using System.Collections.Generic;
using System.Linq;
using System.Web;
using System.Web.Mvc;
using System.Xml.Serialization;
using System.Text;
using System.Xml;
using System.IO;
using System.Web.Script.Serialization;

namespace Curry.Services.Results
{
	/// <report>
	/// Allows returning XML as a result.
	/// </report>
	public class XmlResult : ActionResult
	{
        /// <summary>
        /// The data to serialize as XML
        /// </summary>
		public object Data { get; set; }

		/// <report>
		/// Initializes a new instance of the <see cref="XmlResult"/> class.
		/// </report>
        /// <param name="data">The object to serialize to XML.</param>
		public XmlResult(object data)
		{
			this.Data = data;
		}

		/// <report>
		/// Gets the object to be serialized to XML.
		/// </report>
		public object GetData
		{
			get { return this.Data; }
		}

		/// <report>
		/// Serialises the object that was passed into the constructor to XML and writes the corresponding XML to the result stream.
		/// </report>
		/// <param name="context">The controller context for the current request.</param>
		public override void ExecuteResult(ControllerContext context)
		{
			if (this.Data != null)
			{
                
                // XmlSerializer xs = new XmlSerializer(this.Data.GetType());
                //xs.Serialize(context.HttpContext.Response.Output, this.Data);

                JavaScriptSerializer js = new JavaScriptSerializer { MaxJsonLength = Int32.MaxValue };
                string json = js.Serialize(this.Data);

                XmlDocument xml = Newtonsoft.Json.JsonConvert.DeserializeXmlNode(json, "Data");

                context.HttpContext.Response.Clear();
                context.HttpContext.Response.ContentType = "text/xml";
                context.HttpContext.Response.Output.Write(xml.OuterXml);
			}
		}
	}
}