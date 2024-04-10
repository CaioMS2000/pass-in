import { z } from "zod";
import { ZodTypeProvider } from "fastify-type-provider-zod";
import { prisma } from "../lib/prisma";
import { FastifyInstance } from "fastify";
import { BadRequest } from "./_errors/bad-request";

export async function getEvent(app: FastifyInstance) {
	app.withTypeProvider<ZodTypeProvider>().get(
		"/events/:eventId",
		{
			schema: {
				params: z.object({
					eventId: z.string().uuid(),
					// eventId: z.string(),
				}),
				response: {
					200: z.object({
						event: z.object({
							id: z.string().uuid(),
							title: z.string(),
							slug: z.string(),
							details: z.string().nullable(),
							maximumAttendees: z.number().int().nullable(),
							attendeesAmount: z.number().int(),
						}),
					}),
				},
			},
		},
		async (request, reply) => {
			const { eventId } = request.params;

			const event = await prisma.event.findUnique({
				select: {
					id: true,
					title: true,
					slug: true,
					details: true,
					maximumAttendees: true,
					_count: {
						select: {
							attendees: true,
						},
					},
				},
				where: {
					id: eventId,
				},
			});
			console.log("###");
			console.log(eventId);
			console.log("-----");
			console.log(event);

			if (event === null) throw new BadRequest("Event not found");

			const res = {
				event: {
					id: event.id,
					title: event.title,
					slug: event.slug,
					details: event.details,
					maximumAttendees: event.maximumAttendees,
					attendeesAmount: event._count.attendees,
					// id
					// title
					// slug
					// details
					// maximumAttendees
					// attendeesAmount
				},
			};
			console.log("-----");
			console.log(res);
			console.log("###");

			return reply.send(res);
		}
	);
}
