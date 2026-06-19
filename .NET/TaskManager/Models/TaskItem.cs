using System;
using System.ComponentModel.DataAnnotations;

namespace TaskManager.Models
{
    public class TaskItem
    {
        public int Id { get; set; }

        [Required]
        [Display(Name = "Назва")]
        public string Title { get; set; }

        [Display(Name = "Опис")]
        public string Description { get; set; }

        [Display(Name = "Виконано")]
        public bool IsCompleted { get; set; }

        [Display(Name = "Створено")]
        public DateTime CreatedAt { get; set; } = DateTime.Now;
    }
}
