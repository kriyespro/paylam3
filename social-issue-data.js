const socialIssueDatabase = [
    {
        id: "social-issue",
        title: "Social Issues & Schemes",
        icon: "fas fa-users",
        progress: 0,
        units: [
            { id: "si-unit-1", title: "Related to Vulnerable Sections", lessons: [{title:"Coming Soon", type:"text", completed:false}] },
            { id: "si-unit-2", title: "Related to Human Development and Dignity", lessons: [{title:"Coming Soon", type:"text", completed:false}] },
            { id: "si-unit-3", title: "Related to Society and Its Fabric", lessons: [{title:"Coming Soon", type:"text", completed:false}] },
            { id: "si-unit-4", title: "Types of Schemes", lessons: [{title:"Coming Soon", type:"text", completed:false}] },
            { id: "si-unit-5", title: "Agriculture and Allied Sector", lessons: [{title:"Coming Soon", type:"text", completed:false}] },
            { id: "si-unit-6", title: "Economy and Finance", lessons: [{title:"Coming Soon", type:"text", completed:false}] },
            { id: "si-unit-7", title: "Environment", lessons: [{title:"Coming Soon", type:"text", completed:false}] },
            { id: "si-unit-8", title: "Governance", lessons: [{title:"Coming Soon", type:"text", completed:false}] },
            { id: "si-unit-9", title: "Health and Welfare", lessons: [{title:"Coming Soon", type:"text", completed:false}] },
            { id: "si-unit-10", title: "Human Development", lessons: [{title:"Coming Soon", type:"text", completed:false}] },
            { id: "si-unit-11", title: "Industry and Energy", lessons: [{title:"Coming Soon", type:"text", completed:false}] },
            { id: "si-unit-12", title: "Infrastructure and Communication", lessons: [{title:"Coming Soon", type:"text", completed:false}] },
            { id: "si-unit-13", title: "Science and Technology", lessons: [{title:"Coming Soon", type:"text", completed:false}] }
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
socialIssueDatabase.forEach(subject => {
    subject.progress = calculateProgress(subject);
});






