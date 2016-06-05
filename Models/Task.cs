using System;
using System.Collections.Generic;
using System.Linq;
using System.Web;

namespace Pekaton2016.Models
{
    public class Task
    {
        public int TaskId { get; set; }
        public string TaskName { get; set; }
        public virtual List<Employee> Members { get; set; }
        public virtual List<TaskComment> Comments { get; set; }
        public string Description { get; set; }
        public string EndTime { get; set; }
        public string Done { get; set; }
        public string StartTime { get; set; }
    }
}