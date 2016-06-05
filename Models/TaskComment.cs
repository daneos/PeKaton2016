using System;
using System.Collections.Generic;
using System.Linq;
using System.Web;

namespace Pekaton2016.Models
{
    public class TaskComment
    {
        public string Id { get; set; }
        public string Text { get; set; }
        public virtual Employee User { get; set; }
    }
}