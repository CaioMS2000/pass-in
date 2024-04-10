import { prisma } from '../src/lib/prisma';

async function seed(){
    await prisma.event.create({
        data:{
            title: "Unite Summit",
            slug: "unite-summit",
            details: "Um evento para devs",
            maximumAttendees: 100,
            id: "3f990992-7f48-4002-b59f-d7b08723703c"
        }
    })
}

seed().then(() => {
    console.log('\x1b[32mDatabase seeded \x1b[0m')
    prisma.$disconnect()
})