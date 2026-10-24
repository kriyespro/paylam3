const historyDatabase = [
    {
        id: "ancient",
        title: "Ancient History",
        icon: "fas fa-monument",
        progress: 0,
        units: [
            {
                id: "unit-1",
                title: "Pre-Historic Time",
                lessons: [{title:"Coming Soon", type:"text", completed:false}]
            },
            {
                id: "unit-2",
                title: "Indus Valley Civilization",
                lessons: [{title:"Coming Soon", type:"text", completed:false}]
            },
            { id: "unit-3", title: "Vedic Age", lessons: [{title:"Coming Soon", type:"text", completed:false}] },
            { id: "unit-4", title: "Mahajanapadas", lessons: [{title:"Coming Soon", type:"text", completed:false}] },
            { id: "unit-5", title: "Mauryan Empire", lessons: [{title:"Coming Soon", type:"text", completed:false}] },
            { id: "unit-6", title: "Post-Mauryan Period", lessons: [{title:"Coming Soon", type:"text", completed:false}] },
            { id: "unit-7", title: "Gupta Empire", lessons: [{title:"Coming Soon", type:"text", completed:false}] },
            { id: "unit-8", title: "Harsha Empire", lessons: [{title:"Coming Soon", type:"text", completed:false}] },
            { id: "unit-9", title: "Sangam Age", lessons: [{title:"Coming Soon", type:"text", completed:false}] },
            { id: "unit-10", title: "South Indian Kingdoms", lessons: [{title:"Coming Soon", type:"text", completed:false}] },
            { id: "unit-11", title: "Ancient Religions", lessons: [{title:"Coming Soon", type:"text", completed:false}] },
            { id: "unit-12", title: "Ancient Art & Architecture", lessons: [{title:"Coming Soon", type:"text", completed:false}] },
            { id: "unit-13", title: "Revision", lessons: [{title:"Coming Soon", type:"text", completed:false}] }
        ]
    },
    {
        id: "medieval",
        title: "Medieval History",
        icon: "fas fa-chess-rook",
        progress: 0,
        units: [
            { id: "m-unit-1", title: "Palas", lessons: [{title:"Coming Soon", type:"text", completed:false}] },
            { id: "m-unit-2", title: "Pratiharas", lessons: [{title:"Coming Soon", type:"text", completed:false}] },
            { id: "m-unit-3", title: "Rashtrakutas", lessons: [{title:"Coming Soon", type:"text", completed:false}] },
            { id: "m-unit-4", title: "Delhi Sultanate", lessons: [{title:"Coming Soon", type:"text", completed:false}] },
            { id: "m-unit-5", title: "Vijayanagara Empire", lessons: [{title:"Coming Soon", type:"text", completed:false}] },
            { id: "m-unit-6", title: "Bahmani Kingdom", lessons: [{title:"Coming Soon", type:"text", completed:false}] },
            { id: "m-unit-7", title: "Mughal Empire", lessons: [{title:"Coming Soon", type:"text", completed:false}] },
            { id: "m-unit-8", title: "Marathas", lessons: [{title:"Coming Soon", type:"text", completed:false}] },
            { id: "m-unit-9", title: "Bhakti Movement", lessons: [{title:"Coming Soon", type:"text", completed:false}] },
            { id: "m-unit-10", title: "Sufi Movement", lessons: [{title:"Coming Soon", type:"text", completed:false}] },
            { id: "m-unit-11", title: "Medieval Architecture", lessons: [{title:"Coming Soon", type:"text", completed:false}] },
            { id: "m-unit-12", title: "Revision", lessons: [{title:"Coming Soon", type:"text", completed:false}] }
        ]
    },
    {
        id: "modern",
        title: "Modern History",
        icon: "fas fa-university",
        progress: 0,
        units: [
            { id: "mo-unit-1", title: "Advent of Europeans", lessons: [{title:"Coming Soon", type:"text", completed:false}] },
            { id: "mo-unit-2", title: "Consolidation of British Power", lessons: [{title:"Coming Soon", type:"text", completed:false}] },
            { id: "mo-unit-3", title: "Revolt of 1857", lessons: [{title:"Coming Soon", type:"text", completed:false}] },
            { id: "mo-unit-4", title: "Social & Religious Reforms", lessons: [{title:"Coming Soon", type:"text", completed:false}] },
            { id: "mo-unit-5", title: "INC Formation", lessons: [{title:"Coming Soon", type:"text", completed:false}] },
            { id: "mo-unit-6", title: "Gandhian Era", lessons: [{title:"Coming Soon", type:"text", completed:false}] },
            { id: "mo-unit-7", title: "Revolutionary Movement", lessons: [{title:"Coming Soon", type:"text", completed:false}] },
            { id: "mo-unit-8", title: "Constitutional Development", lessons: [{title:"Coming Soon", type:"text", completed:false}] },
            { id: "mo-unit-9", title: "Partition & Independence", lessons: [{title:"Coming Soon", type:"text", completed:false}] },
            { id: "mo-unit-10", title: "Revision", lessons: [{title:"Coming Soon", type:"text", completed:false}] }
        ]
    },
    {
        id: "art-culture",
        title: "Art & Culture",
        icon: "fas fa-palette",
        progress: 0,
        units: [
            { id: "ac-unit-1", title: "Introduction", lessons: [{title:"Coming Soon", type:"text", completed:false}] },
            { id: "ac-unit-2", title: "Art & Architecture", lessons: [{title:"Coming Soon", type:"text", completed:false}] },
            { id: "ac-unit-3", title: "Temple Architecture", lessons: [{title:"Coming Soon", type:"text", completed:false}] },
            { id: "ac-unit-4", title: "Cave Architecture", lessons: [{title:"Coming Soon", type:"text", completed:false}] },
            { id: "ac-unit-5", title: "Paintings", lessons: [{title:"Coming Soon", type:"text", completed:false}] },
            { id: "ac-unit-6", title: "Sculpture", lessons: [{title:"Coming Soon", type:"text", completed:false}] },
            { id: "ac-unit-7", title: "Music", lessons: [{title:"Coming Soon", type:"text", completed:false}] },
            { id: "ac-unit-8", title: "Dance", lessons: [{title:"Coming Soon", type:"text", completed:false}] },
            { id: "ac-unit-9", title: "Theatre", lessons: [{title:"Coming Soon", type:"text", completed:false}] },
            { id: "ac-unit-10", title: "Puppetry", lessons: [{title:"Coming Soon", type:"text", completed:false}] },
            { id: "ac-unit-11", title: "UNESCO Heritage", lessons: [{title:"Coming Soon", type:"text", completed:false}] },
            { id: "ac-unit-12", title: "Festivals", lessons: [{title:"Coming Soon", type:"text", completed:false}] },
            { id: "ac-unit-13", title: "Literature", lessons: [{title:"Coming Soon", type:"text", completed:false}] },
            { id: "ac-unit-14", title: "Religion & Philosophy", lessons: [{title:"Coming Soon", type:"text", completed:false}] },
            { id: "ac-unit-15", title: "Handicrafts", lessons: [{title:"Coming Soon", type:"text", completed:false}] },
            { id: "ac-unit-16", title: "Revision", lessons: [{title:"Coming Soon", type:"text", completed:false}] }
        ]
    },
    {
        id: "world",
        title: "World History",
        icon: "fas fa-globe-americas",
        progress: 0,
        units: [
            { id: "w-unit-1", title: "Industrial Revolution", lessons: [{title:"Coming Soon", type:"text", completed:false}] },
            { id: "w-unit-2", title: "French Revolution", lessons: [{title:"Coming Soon", type:"text", completed:false}] },
            { id: "w-unit-3", title: "American Revolution", lessons: [{title:"Coming Soon", type:"text", completed:false}] },
            { id: "w-unit-4", title: "Russian Revolution", lessons: [{title:"Coming Soon", type:"text", completed:false}] },
            { id: "w-unit-5", title: "Unification of Germany", lessons: [{title:"Coming Soon", type:"text", completed:false}] },
            { id: "w-unit-6", title: "Unification of Italy", lessons: [{title:"Coming Soon", type:"text", completed:false}] },
            { id: "w-unit-7", title: "World War I", lessons: [{title:"Coming Soon", type:"text", completed:false}] },
            { id: "w-unit-8", title: "World War II", lessons: [{title:"Coming Soon", type:"text", completed:false}] },
            { id: "w-unit-9", title: "Cold War", lessons: [{title:"Coming Soon", type:"text", completed:false}] },
            { id: "w-unit-10", title: "Decolonization", lessons: [{title:"Coming Soon", type:"text", completed:false}] },
            { id: "w-unit-11", title: "Revision", lessons: [{title:"Coming Soon", type:"text", completed:false}] }
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
historyDatabase.forEach(subject => {
    subject.progress = calculateProgress(subject);
});





