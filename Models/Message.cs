using System;
using System.Collections.Generic;
using System.Linq;
using System.Web;

namespace Pekaton2016.Models
{
    public class Message
    {
        public string Id { get; set; }
        public virtual Employee From { get; set; }
        public virtual Employee To { get; set; }
        public string Time { get; set; }
        public string Text { get; set; }
    }
}