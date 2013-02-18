using System;
using System.Web;
using System.Net;
using System.IO;
using System.Text;


namespace Curry.Services
{
    public class CurryRequestRelay
    {
        /// <summary>
        /// Response Http Status Code
        /// </summary>
        public HttpStatusCode HttpStatusCode { get; private set; }
        public string HttpStatusDescription { get; private set; }

        public T RelayRequest<T>(string relayUrl, HttpRequestBase currentReq)
        {

            StringBuilder sbResponse;
            T responseViewModel = default(T);

            var externalRequest = (HttpWebRequest)WebRequest.Create(relayUrl);

            try
            {
                

                //Copy all properties of Original request to the new proxied request

                currentReq.CopyTo(externalRequest);

                // GET HTTP Response
                using (HttpWebResponse response = externalRequest.GetResponse() as HttpWebResponse)
                {
                    this.HttpStatusCode = response.StatusCode;

                    //NonAuthoritativeInformation is 203, which Clouservers API send is sometimes. 203 is almost similar to 200.
                    if (response != null && (response.StatusCode == HttpStatusCode.OK || response.StatusCode == HttpStatusCode.NonAuthoritativeInformation))
                    {
                        // GET HTTP Response Stream
                        using (StreamReader streamReader = new StreamReader(response.GetResponseStream(), Encoding.UTF8))
                        {
                            // Read Response to StringBuilder
                            sbResponse = new StringBuilder(streamReader.ReadToEnd());

                            if (sbResponse.Length > 0)
                            {
                                try
                                {
                                    System.Web.Script.Serialization.JavaScriptSerializer jsonSerializer = new System.Web.Script.Serialization.JavaScriptSerializer { MaxJsonLength = Int32.MaxValue, RecursionLimit = 100 };
                                    responseViewModel = jsonSerializer.Deserialize<T>(sbResponse.ToString());
                                }
                                catch (System.Exception ex)
                                {
                                    throw new System.Exception("Error Parsing Response", ex);
                                }
                            }
                        }
                    }

                    response.Close();
                }
            }
            catch (System.Net.WebException ex)
            {
                if (ex.Response != null)
                {
                    this.HttpStatusCode = ((HttpWebResponse)ex.Response).StatusCode;
                    this.HttpStatusDescription = ((HttpWebResponse)ex.Response).StatusDescription;
                }

                externalRequest.Abort();

            }
            finally
            {
                externalRequest.Abort();
            }
            

            return responseViewModel;
        }
    }
}