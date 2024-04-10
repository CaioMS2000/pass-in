import { z } from "zod";
import { generateSlug } from "../../utils";
import { ZodTypeProvider } from "fastify-type-provider-zod";
import { prisma } from "../lib/prisma";
import { FastifyInstance } from "fastify";
import { BadRequest } from "./_errors/bad-request";

const createEventSchema = z.object({
	title: z.string().min(4),
	details: z.string().nullable(),
	maximumAttendees: z.number().int().positive().nullable(),
});

export async function createEvent(app: FastifyInstance){
    app.withTypeProvider<ZodTypeProvider>().post(
        "/events",
        {
            schema: {
                summary: "Create an event",
                tags: ["events"],
                body: createEventSchema,
                response: { 201: z.object({ eventId: z.string().uuid() }) },
            },
        },
        async (request, reply) => {
            const slug = generateSlug(request.body.title);
            const eventWithSameSlug = await prisma.event.findUnique({
                where: { slug },
            });
    
            if (eventWithSameSlug != null)
                throw new BadRequest("Event with this slug already exists");
    
            const event = await prisma.event.create({
                data: {
                    title: request.body.title,
                    details: request.body.details,
                    maximumAttendees: request.body.maximumAttendees,
                    slug,
                },
            });
    
            // return {eventId: event.id}
            return reply.status(201).send({ eventId: event.id });
        }
    );
}