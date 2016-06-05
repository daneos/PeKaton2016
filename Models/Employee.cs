using System;
using System.Collections.Generic;
using System.Linq;
using System.Web;

namespace Pekaton2016.Models
{
    public class Employee
    {
        public string Name { get; set; }
        public virtual Role Role { get; set; }
        public int EmployeeId { get; set; }
        public virtual List<Event> Events { get; set; }
        public virtual List<Group> Groups { get; set; }
        public string Email { get; set; }
        public string Password { get; set; }
        public virtual Task Task { get; set; }
        public string Points { get; set; }
        public string PointsAva { get; set; }
        public string Hours { get; set; }
        public string HoursGoal { get; set; }
    }
}