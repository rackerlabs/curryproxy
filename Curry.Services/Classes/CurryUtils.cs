using System.Collections.Generic;
using System.Linq;
using System.Web;
using System.Net;
using System.Collections;

namespace Curry.Services
{
    public static class CurryUtils
    {
        /// <summary>
        /// Copies all headers and content (except the URL) from an incoming to an outgoing
        /// request.
        /// </summary>
        /// <param name="source">The request to copy from</param>
        /// <param name="destination">The request to copy to</param>
   
        public static void CopyTo(this HttpRequestBase source, HttpWebRequest destination)
        {
            destination.Method = source.HttpMethod;

            // Copy unrestricted headers (including cookies, if any)
            foreach (var headerKey in source.Headers.AllKeys)
            {
                switch (headerKey)
                {
                    case "Connection":
                    case "Content-Length":
                    case "Date":
                    case "Expect":
                    case "Host":
                    case "If-Modified-Since":
                    case "Range":
                    case "Transfer-Encoding":
                    case "Proxy-Connection":
                        // Let IIS handle these
                        break;

                    case "Accept":
                    case "Content-Type":
                    case "Referer":
                    case "User-Agent":
                        // Restricted - copied below
                        break;

                    default:
                        destination.Headers[headerKey] = source.Headers[headerKey];
                        break;
                }
            }

            // Copy restricted headers
            if (source.AcceptTypes != null)
            {
                if (source.AcceptTypes.Any())
                {
                    destination.Accept = string.Join(",", source.AcceptTypes);
                }
            }

            if (source.UrlReferrer != null)
            {
                destination.Referer = source.UrlReferrer.AbsoluteUri;
            }

            if (source.ContentType != null)
            {
                destination.ContentType = source.ContentType;
            }

            if (source.UserAgent != null)
            {
                destination.UserAgent = source.UserAgent;
            }
            
            

            // Copy content (if content body is allowed)
            if (source.HttpMethod != "GET"
                && source.HttpMethod != "HEAD"
                && source.ContentLength > 0)
            {
                var destinationStream = destination.GetRequestStream();
                source.InputStream.CopyTo(destinationStream);
                destinationStream.Close();
            }
        }


    }
   
    public class ChainedEnumerable<T> : IEnumerable<T>
    {
        private readonly IEnumerable<T>[] _inners;

        public ChainedEnumerable(params IEnumerable<T>[] inners)
        {
            _inners = inners;
        }

        public IEnumerator<T> GetEnumerator()
        {
            foreach (IEnumerable<T> inner in _inners)
            {
                foreach (T t in inner)
                {
                    yield return t;
                }
            }
        }

        IEnumerator IEnumerable.GetEnumerator()
        {
            return GetEnumerator();
        }
    }
}