const governanceDatabase = [
    {
        id: "governance",
        title: "Governance",
        icon: "fas fa-balance-scale",
        progress: 0,
        units: [
            { id: "g-unit-1", title: "Governance: Concepts and Framework", lessons: [{title:"Coming Soon", type:"text", completed:false}] },
            { id: "g-unit-2", title: "Transparency and Accountability", lessons: [{title:"Coming Soon", type:"text", completed:false}] },
            { id: "g-unit-3", title: "Development Processes and Stakeholders", lessons: [{title:"Coming Soon", type:"text", completed:false}] },
            { id: "g-unit-4", title: "Pressure Groups and Civil Society", lessons: [{title:"Coming Soon", type:"text", completed:false}] },
            { id: "g-unit-5", title: "Role of Civil Services in a Democracy", lessons: [{title:"Coming Soon", type:"text", completed:false}] }
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
governanceDatabase.forEach(subject => {
    subject.progress = calculateProgress(subject);
});






