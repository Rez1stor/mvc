using Microsoft.AspNetCore.Mvc;
using System.Diagnostics;
using TaskManager.Models;

namespace TaskManager.Controllers
{
    public class HomeController : Controller
    {
        private static List<TaskItem> _tasks = new List<TaskItem>();
        private static int _nextId = 1;

        public IActionResult Index()
        {
            return View(_tasks);
        }

        [HttpPost]
        public IActionResult Create(TaskItem task)
        {
            if (ModelState.IsValid)
            {
                task.Id = _nextId++;
                task.CreatedAt = System.DateTime.Now;
                _tasks.Add(task);
                return RedirectToAction(nameof(Index));
            }
            return View("Index", _tasks);
        }

        [ResponseCache(Duration = 0, Location = ResponseCacheLocation.None, NoStore = true)]
        public IActionResult Error()
        {
            return View(new ErrorViewModel { RequestId = Activity.Current?.Id ?? HttpContext.TraceIdentifier });
        }
    }
}
