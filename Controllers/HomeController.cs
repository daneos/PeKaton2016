using Pekaton2016.Models;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Net.Http;
using System.Net.Http.Headers;
using System.Security.Cryptography;
using System.Text;
using System.Threading.Tasks;
using System.Web;
using System.Web.Mvc;

namespace Pekaton2016.Controllers
{
    public class HomeController : Controller
    {
        private readonly string ServerUri = "http://192.168.1.150:8000/";
        public string SessionId { get; set; }

        private async Task<List<Message>> GetMessages()
        {
            // http://192.168.1.150:8000/api/rest/v1/messages/42f5ada7-833f-4640-ae67-9d770d39c372/
            SessionId = (string)Session["id"];

            List<Message> messages = new List<Message>();
            using (var client = new HttpClient())
            {
                client.BaseAddress = new Uri(ServerUri);
                client.DefaultRequestHeaders.Accept.Clear();
                client.DefaultRequestHeaders.Accept.Add(new MediaTypeWithQualityHeaderValue("application/json"));

                var response2 = await client.GetAsync("api/rest/v1/messages/" + SessionId + "/");
                dynamic mgs = await response2.Content.ReadAsAsync<object>();
                foreach(dynamic msg in mgs["data"])
                {
                    string date = (string)msg["time"];
                    string fromid = (string)msg["from"];
                    string toid = (string)msg["to"];
                    string id = (string)msg["id"];
                    string text = (string)msg["text"];
                    // text

                    Employee from = await this.GetEmployee(fromid);
                    Employee to = await this.GetEmployee(toid);
                    Message message = new Message();
                    message.From = from;
                    message.To = to;
                    message.Time = date;
                    message.Id = id;
                    message.Text = text;
                    messages.Add(message);
                }
            }
            return messages;
        }

        private async Task<Models.Task> GetTask(string id)
        {
            SessionId = (string)Session["id"];
            Models.Task t = new Models.Task();

            using (var client = new HttpClient())
            {
                client.BaseAddress = new Uri(ServerUri);
                client.DefaultRequestHeaders.Accept.Clear();
                client.DefaultRequestHeaders.Accept.Add(new MediaTypeWithQualityHeaderValue("application/json"));

                var response2 = await client.GetAsync("api/rest/v1/tasks/" + SessionId + "/" + id + "/");
                dynamic task = await response2.Content.ReadAsAsync<object>();

                string deadline = (string)task["data"]["deadline"];
                string name = (string)task["data"]["name"];
                string done = (string)task["data"]["done"];
                int idd = Convert.ToInt32((string)task["data"]["id"]);
                string starttime = (string)task["data"]["time_start"];
                string desc = (string)task["data"]["description"];
                t.Description = desc;
                t.StartTime = starttime;
                t.EndTime = deadline;
                t.TaskId = idd;
                t.Done = done;
                t.TaskName = name;
                List<TaskComment> taskComments = new List<TaskComment>();

                foreach (dynamic taskcmnt in task["data"]["comments"])
                {
                    TaskComment tc = new TaskComment();
                    string text = (string)taskcmnt["text"];
                    string tcid = (string)taskcmnt["id"];
                    string user = (string)taskcmnt["user"];

                    Employee taskCommentator = await this.GetEmployee(user);
                    tc.Id = tcid;
                    tc.Text = text;
                    tc.User = taskCommentator;

                    taskComments.Add(tc);
                }
                t.Comments = taskComments;
                List<Employee> members = new List<Employee>();
                foreach (dynamic member in task["data"]["members"])
                {
                    string memberid = (string)member["user"];
                    string roleid = (string)member["role"];
                    Role role = await this.GetRole(roleid);
                    Employee memb = await this.GetEmployee(memberid);
                    memb.Role = role;

                    members.Add(memb);

                }
                t.Members = members;


            }
            return t;
        }

        private async Task<List<Pekaton2016.Models.Task>> GetAllTasks()
        {
            SessionId = (string)Session["id"];
            List<Pekaton2016.Models.Task> tasks = new List<Pekaton2016.Models.Task>();
            using (var client = new HttpClient())
            {
                client.BaseAddress = new Uri(ServerUri);
                client.DefaultRequestHeaders.Accept.Clear();
                client.DefaultRequestHeaders.Accept.Add(new MediaTypeWithQualityHeaderValue("application/json"));

                var response2 = await client.GetAsync("api/rest/v1/tasks/" + SessionId + "/");
                dynamic status2 = await response2.Content.ReadAsAsync<object>();

                foreach(dynamic task in status2["data"])
                {
                    Pekaton2016.Models.Task t = new Models.Task();

                    string deadline = (string)task["deadline"];
                    string name = (string)task["name"];
                    string done = (string)task["done"]; 
                    int id = Convert.ToInt32((string)task["id"]);
                    t.EndTime = deadline.Substring(0, deadline.Length -3);
                    t.TaskName = name;
                    t.Done = done;
                    t.TaskId = id;
                    tasks.Add(t);
                }
            }
            return tasks;
        }

        private async Task<List<Employee>> GetAllEmployees()
        {
            SessionId = (string)Session["id"];
            List<Employee> employees = new List<Employee>();
            using (var client = new HttpClient())
            {
                client.BaseAddress = new Uri(ServerUri);
                client.DefaultRequestHeaders.Accept.Clear();
                client.DefaultRequestHeaders.Accept.Add(new MediaTypeWithQualityHeaderValue("application/json"));

                var response2 = await client.GetAsync("api/rest/v1/users/" + SessionId + "/");
                dynamic status2 = await response2.Content.ReadAsAsync<object>();

                foreach (var empl in status2["data"])
                {
                    Employee emp = new Employee();
                    string email = (string)empl["email"];
                    string name = (string)empl["name"];
                    int idE = Convert.ToInt32((string)empl["id"]);
                    string hours = (string)empl["hours"];
                    string hoursgoal = (string)empl["hour_goal"];
                    string points = (string)empl["points"];
                    string pointsAva = (string)empl["points_available"];

                    emp.Hours = hours;
                    emp.HoursGoal = hoursgoal;
                    emp.Points = points;
                    emp.PointsAva = pointsAva;
                    emp.Email = email;
                    emp.Name = name;
                    emp.EmployeeId = idE;
                    employees.Add(emp);
                }

            }
            return employees;

        }
        private async Task<Employee> GetEmployee(string id)
        {
            SessionId = (string)Session["id"];
            Employee emp = new Employee();
            using (var client = new HttpClient())
            {
                client.BaseAddress = new Uri(ServerUri);
                client.DefaultRequestHeaders.Accept.Clear();
                client.DefaultRequestHeaders.Accept.Add(new MediaTypeWithQualityHeaderValue("application/json"));

                var response2 = await client.GetAsync("api/rest/v1/users/" + SessionId + "/" + id + "/");
                dynamic status2 = await response2.Content.ReadAsAsync<object>();

                string email = (string)status2["data"]["email"];
                string name = (string)status2["data"]["name"];
                int idE = Convert.ToInt32((string)status2["data"]["id"]);
                string hours = (string)status2["data"]["hours"];
                string hoursgoal = (string)status2["data"]["hour_goal"];
                string points = (string)status2["data"]["points"];
                string pointsAva = (string)status2["data"]["points_available"];

                emp.Hours = hours;
                emp.HoursGoal = hoursgoal;
                emp.Points = points;
                emp.PointsAva = pointsAva;
                emp.Email = email;
                emp.Name = name;
                emp.EmployeeId = idE;
            }
            return emp;

        }
        private async Task<Role> GetRole(string id)
        {
            SessionId = (string)Session["id"];
            Role role = new Role();
            using (var client = new HttpClient())
            {
                client.BaseAddress = new Uri(ServerUri);
                client.DefaultRequestHeaders.Accept.Clear();
                client.DefaultRequestHeaders.Accept.Add(new MediaTypeWithQualityHeaderValue("application/json"));

                var response2 = await client.GetAsync("api/rest/v1/roles/" + SessionId + "/" + id + "/");
                dynamic status2 = await response2.Content.ReadAsAsync<object>();

                string description = (string)status2["data"]["description"];
                string name = (string)status2["data"]["name"];
                int idE = Convert.ToInt32((string)status2["data"]["id"]);

                role.RoleId = idE;
                role.Description = description;
                role.Name = name;
            }
            return role;

        }


        private static long ConvertToTimestamp(DateTime value)
        {
            long epoch = (value.Ticks - 621355968000000000) / 10000000;
            return epoch;
        }

        public ActionResult Index()
        {
            return View();
        }

        public ActionResult About()
        {
            ViewBag.Message = "Your application description page.";

            return View();
        }

        public ActionResult Contact()
        {
            ViewBag.Message = "Your contact page.";

            return View();
        }
        [HttpGet]
        public ActionResult Login()
        {
            return View();
        }

        [HttpPost]
        public async Task<ActionResult> Login(string Email, string Password)
        {
            var sha1 = new SHA1CryptoServiceProvider();
            var data = Encoding.ASCII.GetBytes(Password);
            var passHashB = sha1.ComputeHash(data);
            //var passHash = Convert.(sha1.ComputeHash(passHashB));
            var passHash = BitConverter.ToString(passHashB).Replace("-", "").ToLower();

            using (var client = new HttpClient())
            {
                client.BaseAddress = new Uri(ServerUri);
                client.DefaultRequestHeaders.Accept.Clear();
                client.DefaultRequestHeaders.Accept.Add(new MediaTypeWithQualityHeaderValue("application/json"));


                HttpResponseMessage response = await client.GetAsync("api/rest/v1/login?email=" + Email + "&password=" + passHash);
                if (response.IsSuccessStatusCode)
                {
                    dynamic status = await response.Content.ReadAsAsync<object>();

                    if ((string)status["status"] == "ERROR")
                    {
                        ViewData["error"] = (string)status["reason"];
                        return View();
                    }
                    else
                    {
                        Session["id"] = (string)status["data"]["session_id"];
                        SessionId = (string)status["data"]["session_id"];
                        Session["userid"] = (string)status["data"]["user"];
                        string userId = (string)status["data"]["user"];
                        var response2 = await client.GetAsync("api/rest/v1/users/" + SessionId + "/" + userId + "/");
                        dynamic status2 = await response2.Content.ReadAsAsync<object>();

                        string email = (string)status2["data"]["email"];
                        string name = (string)status2["data"]["name"];
                        string hours = (string)status2["data"]["hours"];
                        string hoursgoal = (string)status2["data"]["hour_goal"];
                        string points = (string)status2["data"]["points"];
                        string pointsAva = (string)status2["data"]["points_available"];

                        int id = Convert.ToInt32((string)status2["data"]["id"]);
                        Employee emp = new Employee()
                        {
                            Email = email,
                            Name = name,
                            EmployeeId = id,
                            Points = points,
                            PointsAva = pointsAva,
                            Hours = hours,
                            HoursGoal = hoursgoal
                        };
                        Session["signedin"] = "false";
                        Session["pointsava"] = emp.PointsAva;
                        Session["user"] = emp;
                        List<Employee> employees = await this.GetAllEmployees();
                        List<Message> messages = await this.GetMessages();
                        Session["employees"] = employees;
                        Session["messages"] = messages;

                        return View("Manage", emp);
                    }
                }
                else
                {
                    Session["error"] = "Something went wrong";
                }
            }
            return View();
        }

        [HttpGet]
        public async Task<ActionResult> Manage()
        {
            if (Session["user"] == null)
            {
                return RedirectToAction("Login");
            }
            else
            {
                Employee emp = (Employee)Session["user"];
                string id = (emp.EmployeeId).ToString();
                //api/rest/v1/users/[session-id]/
             

                emp = await this.GetEmployee(id);
                return View(emp);
            }
        }
        [HttpGet]
        public async Task<ActionResult> Rooms()
        {

            if (Session["user"] == null)
            {
                return RedirectToAction("Login");
            }
            else
            {
                using (var client = new HttpClient())
                {
                    client.BaseAddress = new Uri(ServerUri);
                    client.DefaultRequestHeaders.Accept.Clear();
                    client.DefaultRequestHeaders.Accept.Add(new MediaTypeWithQualityHeaderValue("application/json"));

                    // http://192.168.16.115:8000/api/rest/v1/rooms/c5d658b7-7eb4-45e7-9ac6-679acaf7e34b/
                    SessionId = (string)Session["id"];
                    HttpResponseMessage response = await client.GetAsync("api/rest/v1/rooms/" + SessionId + "/");
                    if (response.IsSuccessStatusCode)
                    {
                        dynamic status = await response.Content.ReadAsAsync<object>();
                        List<Room> rooms = new List<Room>();
                        foreach (dynamic room in status["data"])
                        {
                            Room newR = new Room();
                            newR.Description = (string)room["description"];
                            newR.RoomId = Convert.ToInt32((string)room["id"]);
                            newR.Name = (string)room["name"];
                            rooms.Add(newR);
                        }
                        return View(rooms);
                    }
                }
                return View();
            }
        }
        [HttpGet]
        public async Task<ActionResult> Room(int roomId)
        {
            Session["roomid"] = roomId;
            if (Session["user"] != null)
            {
                using (var client = new HttpClient())
                {
                    client.BaseAddress = new Uri(ServerUri);
                    client.DefaultRequestHeaders.Accept.Clear();
                    client.DefaultRequestHeaders.Accept.Add(new MediaTypeWithQualityHeaderValue("application/json"));

                    // http://192.168.16.115:8000/api/rest/v1/rooms/c5d658b7-7eb4-45e7-9ac6-679acaf7e34b/
                    SessionId = (string)Session["id"];
                    HttpResponseMessage response = await client.GetAsync("api/rest/v1/rooms/" + SessionId + "/" + roomId + "/");
                    if (response.IsSuccessStatusCode)
                    {
                        dynamic status = await response.Content.ReadAsAsync<object>();
                        List<RoomTimeSpan> timetable = new List<RoomTimeSpan>();
                        foreach (dynamic roomtimespan in status["data"]["timetable"])
                        {
                            string id = (string)roomtimespan["owner"];
                            var response2 = await client.GetAsync("api/rest/v1/users/" + SessionId + "/" + id + "/");
                            dynamic status2 = await response2.Content.ReadAsAsync<object>();

                            string email = (string)status2["data"]["email"];
                            string name = (string)status2["data"]["name"];
                            int idU = Convert.ToInt32(id);
                            Employee emp = new Employee()
                            {
                                Email = email,
                                Name = name,
                                EmployeeId = idU
                            };

                            RoomTimeSpan rts = new RoomTimeSpan();

                            string startTime = ((string)roomtimespan["time_start"]).Replace("+00:00", "");
                            string endTime = ((string)roomtimespan["time_end"]).Replace("+00:00", "");

                            //rts.StartTime = DateTime.ParseExact(startTime, "yyyy -MM-dd HH:mm:ss,fff", System.Globalization.CultureInfo.InvariantCulture);
                            //rts.EndTime = DateTime.ParseExact(endTime, "yyyy -MM-dd HH:mm:ss,fff", System.Globalization.CultureInfo.InvariantCulture);
                            rts.EndTimeS = endTime;
                            rts.StartTimeS = startTime;
                            rts.Owner = emp;
                            rts.RoomId = roomId.ToString();

                            timetable.Add(rts);

                        }
                        return View("RoomDetails", timetable);
                    }
                    else
                    {
                        return RedirectToAction("Rooms");
                    }
                }
            }
            else
            {
                RedirectToAction("Login");
            }
            return RedirectToAction("Rooms");


        }
        [HttpPost]
        public async Task<ActionResult> ReserveRoom(string startDate, string startTime, string endDate, string endTime, string roomId)
        {
            string startS = (startDate + " " + startTime);
            DateTime startD = DateTime.ParseExact(startS, "yyyy-MM-dd HH:mm", null);
            DateTime endD = DateTime.ParseExact((endDate + " " + endTime), "yyyy-MM-dd HH:mm", null);

            long startInt = ConvertToTimestamp(startD);
            long endInt = ConvertToTimestamp(endD);

            SessionId = (string)Session["id"];

            using (var client = new HttpClient())
            {
                client.BaseAddress = new Uri(ServerUri);
                client.DefaultRequestHeaders.Accept.Clear();
                client.DefaultRequestHeaders.Accept.Add(new MediaTypeWithQualityHeaderValue("application/json"));

                // http://localhost:8000/api/rest/v1/rooms/66b5f696-e01c-46f0-a55f-16b393f6ea84/2/register/?start=1465049225&end=1465059225
                SessionId = (string)Session["id"];
                HttpResponseMessage response = await client.GetAsync("api/rest/v1/rooms/" + SessionId + "/" + roomId + "/register/?start=" + startInt + "&end=" + endInt);
                if (response.IsSuccessStatusCode)
                {
                    ViewData["message"] = "You have reserved a room";
                    return RedirectToAction("Rooms");
                }
            }

            return RedirectToAction("Rooms");
        }
        public async Task<ActionResult> Vouchers()
        {
            if (Session["user"] != null)
            {
                using (var client = new HttpClient())
                {
                    client.BaseAddress = new Uri(ServerUri);
                    client.DefaultRequestHeaders.Accept.Clear();
                    client.DefaultRequestHeaders.Accept.Add(new MediaTypeWithQualityHeaderValue("application/json"));

                    // http://localhost:8000/api/rest/v1/rooms/66b5f696-e01c-46f0-a55f-16b393f6ea84/2/register/?start=1465049225&end=1465059225
                    SessionId = (string)Session["id"];
                    HttpResponseMessage response = await client.GetAsync("api/rest/v1/food/" + SessionId + "/");
                    if (response.IsSuccessStatusCode)
                    {
                        dynamic status = await response.Content.ReadAsAsync<object>();
                        List<Voucher> vouchers = new List<Voucher>();
                        foreach (dynamic vs in status["data"])
                        {
                            Voucher v = new Voucher();
                            v.Thumb = (string)vs["thumb"];
                            v.Name = (string)vs["name"];
                            v.VoucherId = Convert.ToInt32((string)vs["id"]);
                            vouchers.Add(v);
                        }
                        return View(vouchers);
                    }
                    else
                    {
                        return RedirectToAction("Login");
                    }
                }
            }
            else
            {
                return RedirectToAction("Login");
            }
        }
        [HttpGet]
        public async Task<ActionResult> VoucherInfo(string id)
        {
            using (var client = new HttpClient())
            {
                client.BaseAddress = new Uri(ServerUri);
                client.DefaultRequestHeaders.Accept.Clear();
                client.DefaultRequestHeaders.Accept.Add(new MediaTypeWithQualityHeaderValue("application/json"));

                // http://localhost:8000/api/rest/v1/rooms/66b5f696-e01c-46f0-a55f-16b393f6ea84/2/register/?start=1465049225&end=1465059225
                SessionId = (string)Session["id"];
                HttpResponseMessage response = await client.GetAsync("api/rest/v1/food/" + SessionId + "/" + id + "/");
                if (response.IsSuccessStatusCode)
                {
                    dynamic status = await response.Content.ReadAsAsync<object>();
                    Voucher v = new Voucher();
                    string thumb = (string)status["data"]["thumb"];
                    string name = (string)status["data"]["name"];
                    string code = (string)status["data"]["code"];
                    string desc = (string)status["data"]["description"];
                    v.Thumb = thumb;
                    v.Name = name;
                    v.Code = code;
                    v.Description = desc;

                    return View(v);
                }
                else
                {
                    return RedirectToAction("Vouchers");
                }
            }
        }
        public async Task<ActionResult> ParkingSpots()
        {
            if (Session["user"] != null)
            {
                using (var client = new HttpClient())
                {
                    client.BaseAddress = new Uri(ServerUri);
                    client.DefaultRequestHeaders.Accept.Clear();
                    client.DefaultRequestHeaders.Accept.Add(new MediaTypeWithQualityHeaderValue("application/json"));

                    SessionId = (string)Session["id"];
                    HttpResponseMessage response = await client.GetAsync("api/rest/v1/parkspots/" + SessionId + "/");
                    if (response.IsSuccessStatusCode)
                    {
                        dynamic status = await response.Content.ReadAsAsync<object>();
                        List<ParkSpot> parkSpots = new List<ParkSpot>();
                        foreach (dynamic pss in status["data"])
                        {
                            ParkSpot ps = new ParkSpot();
                            ps.Location = (string)pss["location"];
                            ps.ParkSpotId = (string)pss["id"];
                            ps.Spot = (string)pss["spot"];
                            ps.OwnerId = (string)pss["user"];
                            parkSpots.Add(ps);
                        }
                        return View(parkSpots);
                    }
                    else
                    {
                        return RedirectToAction("Login");
                    }
                }
            }
            else
            {
                return RedirectToAction("Login");
            }
        }
        public async Task<ActionResult> ReserveParkingSpot(string id)
        {
            using (var client = new HttpClient())
            {
                client.BaseAddress = new Uri(ServerUri);
                client.DefaultRequestHeaders.Accept.Clear();
                client.DefaultRequestHeaders.Accept.Add(new MediaTypeWithQualityHeaderValue("application/json"));

                SessionId = (string)Session["id"];
                HttpResponseMessage response = await client.GetAsync("api/rest/v1/parkspots/" + SessionId + "/" + id + "/take/");
                Session["message"] = "Congratulations ! You have reserved a parking spot";
                return RedirectToAction("ParkingSpots");
            }
        }
        public async Task<ActionResult> FreeParkingSpot(string id)
        {
            using (var client = new HttpClient())
            {
                client.BaseAddress = new Uri(ServerUri);
                client.DefaultRequestHeaders.Accept.Clear();
                client.DefaultRequestHeaders.Accept.Add(new MediaTypeWithQualityHeaderValue("application/json"));

                SessionId = (string)Session["id"];
                HttpResponseMessage response = await client.GetAsync("api/rest/v1/parkspots/" + SessionId + "/" + id + "/free/");
                Session["message"] = "Congratulations ! You have freed a parking spot";
                return RedirectToAction("ParkingSpots");
            }
        }
        public async Task<ActionResult> Groups()
        {
            if (Session["user"] != null)
            {
                using (var client = new HttpClient())
                {
                    client.BaseAddress = new Uri(ServerUri);
                    client.DefaultRequestHeaders.Accept.Clear();
                    client.DefaultRequestHeaders.Accept.Add(new MediaTypeWithQualityHeaderValue("application/json"));

                    SessionId = (string)Session["id"];
                    HttpResponseMessage response = await client.GetAsync("api/rest/v1/groups/" + SessionId + "/");
                    if (response.IsSuccessStatusCode)
                    {
                        List<Group> groups = new List<Group>();
                        dynamic status = await response.Content.ReadAsAsync<object>();
                        foreach (dynamic group in status["data"])
                        {
                            List<Employee> members = new List<Employee>();
                            Group g = new Group();
                            g.GroupId = group["id"];
                            g.GroupName = group["name"];
                            int i = 0;
                            foreach (dynamic member in group["members"])
                            {
                                string id = (string)member["user"];
                                string role = (string)member["role"];
                                Employee ne = await this.GetEmployee(id);
                                ne.Role = await this.GetRole(role);
                                i++;
                                members.Add(ne);
                            }
                            g.Members = members;
                            groups.Add(g);
                        }
                        return View(groups);

                    }
                    else
                    {
                        return RedirectToAction("Login");
                    }
                }
            }
            else
            {
                return RedirectToAction("Login");
            }
        }
        public async Task<ActionResult> Employees()
        {
            if (Session["user"] != null)
            {
                var employees = await this.GetAllEmployees();
                return View(employees);
            }
            else
            {
                return RedirectToAction("Login");
            }
        }
        [HttpGet]
        public async Task<ActionResult> BestowPoints()
        {
            if (Session["user"] != null)
            {
                var users = await this.GetAllEmployees();

                return View(users);
            }
            else
            {
                return RedirectToAction("Login");
            }
        }
        [HttpPost]
        public async Task<ActionResult> BestowPoints(string points, string id)
        {
            using (var client = new HttpClient())
            {
                client.BaseAddress = new Uri(ServerUri);
                client.DefaultRequestHeaders.Accept.Clear();
                client.DefaultRequestHeaders.Accept.Add(new MediaTypeWithQualityHeaderValue("application/json"));

                SessionId = (string)Session["id"];
                HttpResponseMessage response = await client.GetAsync("api/rest/v1/users/" + SessionId + "/" + id + "/kudos/?points=" + points);
                if (response.IsSuccessStatusCode)
                {
                    TempData["message"] = "Congratulations ! You have bestow points";
                }
                else
                {
                    TempData["message"] = "Something went wrong";
                }
            }
            return RedirectToAction("Manage");
        }

        public async Task<ActionResult> Tasks()
        {
            if(Session["user"] !=null)
            {
                var tasks = await this.GetAllTasks();
                return View(tasks);
            }
            else
            {
                return RedirectToAction("login");
            }
        }

        [HttpGet]
        public async Task<ActionResult> TaskDetails(string id)
        {
            if(Session["user"] != null)
            {
                var task = await this.GetTask(id);
                return View(task);
            }
            else
            {
                return RedirectToAction("login");
            }
        }

        [HttpPost]
        public async Task<ActionResult> TaskDetails(string text, string id)
        {
            using (var client = new HttpClient())
            {
                client.BaseAddress = new Uri(ServerUri);
                client.DefaultRequestHeaders.Accept.Clear();
                client.DefaultRequestHeaders.Accept.Add(new MediaTypeWithQualityHeaderValue("application/json"));

                SessionId = (string)Session["id"];
                //http://localhost:8000/api/rest/v1/tasks/[session-id]/[task-id]/comment/?text=[comment]
                HttpResponseMessage response = await client.GetAsync("api/rest/v1/tasks/" + SessionId + "/" + id + "/comment/?text=" + text);
                Session["comment"] = "Congratulations ! You have added a comment.";

            }
            return RedirectToAction("TaskDetails", new { id = id });
        }
        [HttpGet]
        public async Task<ActionResult> EditTask(string id)
        {
            if(Session["user"] != null)
            {
                var task = await this.GetTask(id);
                return View(task);
            }
            else
            {
                return RedirectToAction("login");
            }
        }
        [HttpPost]
        public async Task<ActionResult> EditTask(string TaskName, string Description, string EndTime, string Done, string TaskId)
        {
            using (var client = new HttpClient())
            {
                client.BaseAddress = new Uri(ServerUri);
                client.DefaultRequestHeaders.Accept.Clear();
                client.DefaultRequestHeaders.Accept.Add(new MediaTypeWithQualityHeaderValue("application/json"));

                SessionId = (string)Session["id"];
                //http://localhost:8000/api/rest/v1/tasks/[session-id]/[task-id]/comment/?text=[comment]
                HttpResponseMessage response = await client.GetAsync("api/rest/v1/tasks/" + SessionId + "/" + TaskId + "/update/?name=" + TaskName + "&description=" + Description + "&deadline=" + EndTime + "&done=" + Done);
                Session["comment"] = "Congratulations ! You have edited a task";

            }
            return RedirectToAction("TaskDetails", new { id = TaskId });
        }

        public async Task<ActionResult> Messages()
        {
            if (Session["user"] != null)
            {
                var messages = await this.GetMessages();
                return View(messages);
            }
            else
            {
                return RedirectToAction("login");
            }
        }
        public async Task<ActionResult> StartSession()
        {
            if(Session["user"] != null)
            {
                using (var client = new HttpClient())
                {
                    client.BaseAddress = new Uri(ServerUri);
                    client.DefaultRequestHeaders.Accept.Clear();
                    client.DefaultRequestHeaders.Accept.Add(new MediaTypeWithQualityHeaderValue("application/json"));

                    SessionId = (string)Session["id"];
                    //http://localhost:8000/api/rest/v1/tasks/[session-id]/[task-id]/comment/?text=[comment]
                    HttpResponseMessage response = await client.GetAsync("api/rest/v1/time_start/" + SessionId + "/");
                    Session["comment"] = "Congratulations ! You have signed in";
                    Session["signedin"] = "true";

                }
                return RedirectToAction("Manage");
            }
            else
            {
                return RedirectToAction("login");
            }
        }

        public async Task<ActionResult> EndSession()
        {
            if (Session["user"] != null)
            {
                using (var client = new HttpClient())
                {
                    client.BaseAddress = new Uri(ServerUri);
                    client.DefaultRequestHeaders.Accept.Clear();
                    client.DefaultRequestHeaders.Accept.Add(new MediaTypeWithQualityHeaderValue("application/json"));

                    SessionId = (string)Session["id"];
                    //http://localhost:8000/api/rest/v1/tasks/[session-id]/[task-id]/comment/?text=[comment]
                    HttpResponseMessage response = await client.GetAsync("api/rest/v1/time_stop/" + SessionId + "/");
                    Session["comment"] = "Congratulations ! You have signed out";
                    Session["signedin"] = "false";

                }
                return RedirectToAction("Manage");
            }
            else
            {
                return RedirectToAction("login");
            }
        }
    }
}