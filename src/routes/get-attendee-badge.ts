import { z } from "zod";
import { ZodTypeProvider } from "fastify-type-provider-zod";
import { prisma } from "../lib/prisma";
import { FastifyInstance } from "fastify";
import { BadRequest } from "./_errors/bad-request";

export async function getAttendeeBadge(app: FastifyInstance) {
	app.withTypeProvider<ZodTypeProvider>().get("/attendees/:attendeeId/badge", {schema:{
        params: z.object({
            // attendeeId: z.string().transform(Number).int(),
            attendeeId: z.coerce.number().int(),
        }),
        response: {
            200: z.object({
                badge: z.object({
                    name: z.string(),
                    email: z.string().email(),
                    eventTitle: z.string(),
                    checkInURL: z.string().url(),
                })
            })
        }
    }}, async (request, reply) => {
        const {attendeeId} = request.params

        const attendee = await prisma.attendee.findUnique({
            where:{
                id: attendeeId
            },
            select:{
                name: true,
                email: true,
                event:{
                    select:{
                        title: true
                    }
                }
            }
        })

        if(attendee === null) throw new BadRequest("Attendee not found");

        const baseURL = `${request.protocol}://${request.hostname}`
        const checkInURL = new URL(`/attendees/${attendeeId}/check-in`, baseURL)

        return reply.send({badge: {
            name: attendee.name,
            email: attendee.email,
            eventTitle: attendee.event.title,
            checkInURL: checkInURL.toString()
        }})
    })
}