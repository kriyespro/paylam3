const disasterDatabase = [
    {
        id: "disaster-management",
        title: "Disaster Management",
        icon: "fas fa-house-damage",
        progress: 0,
        units: [
            { 
                id: "dm-unit-1", 
                title: "Foundations of Disaster Management", 
                lessons: [
                    {title:"Lesson 1", type:"text", completed:false},
                    {title:"Lesson 2", type:"video", completed:false}
        ] 
            },
            { 
                id: "dm-unit-2", 
                title: "Specific Disasters and Hazard-wise Management", 
                lessons: [
                    {title:"Lesson 1", type:"text", completed:false},
                    {title:"Lesson 2", type:"video", completed:false}
        ] 
            },
            { 
                id: "dm-unit-3", 
                title: "Institutional and Legal Framework", 
                lessons: [
                    {title:"Lesson 1", type:"text", completed:false},
                    {title:"Lesson 2", type:"video", completed:false}
        ] 
            },
            { 
                id: "dm-unit-4", 
                title: "Enabling Mechanisms in Disaster Management", 
                lessons: [
                    {title:"Lesson 1", type:"text", completed:false},
                    {title:"Lesson 2", type:"video", completed:false}
        ] 
            }
        ]
    },
    {
        id: "final-revision-section",
        title: "Final Revision",
        icon: "fas fa-check-double",
        progress: 0,
        units: [
            { id: "final-rev-1", title: "Complete units Revision", lessons: [{title:"Coming Soon", type:"text", completed:false}] },
            { id: "final-rev-2", title: "Mock Tests & Practice", lessons: [{title:"Coming Soon", type:"text", completed:false}] }
        ]
    }
];

// Utility function to calculate overall progress of a subject based on completed lessons
function calculateProgress(subject) {
    let totalLessons = 0;
    let completedLessons = 0;

    subject.units.forEach(unit => {
        totalLessons += unit.lessons.length;
        completedLessons += unit.lessons.filter(l => l.completed).length;
    });

    if (totalLessons === 0) return 0;
    return Math.round((completedLessons / totalLessons) * 100);
}

// Pre-calculate progress for all subjects on load
disasterDatabase.forEach(subject => {
    subject.progress = calculateProgress(subject);
});






