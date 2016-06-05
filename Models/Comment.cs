using System;
using System.Collections.Generic;
using System.Linq;
using System.Web;

namespace Pekaton2016.Models
{
    public class Comment
    {
        public virtual Employee Commentator { get; set; }
        public string Body { get; set; }
    }
}