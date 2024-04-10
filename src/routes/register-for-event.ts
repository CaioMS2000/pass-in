import { z } from "zod";
import { ZodTypeProvider } from "fastify-type-provider-zod";
import { prisma } from "../lib/prisma";
import { FastifyInstance } from "fastify";
import { BadRequest } from "./_errors/bad-request";

export async function registerForEvent(app: FastifyInstance) {
	app.withTypeProvider<ZodTypeProvider>().post(
		"/events/:eventId/attendees",
		{
			schema: {
				body: z.object({
					name: z.string().min(4),
					email: z.string().email(),
				}),
				params: z.object({
					eventId: z.string().uuid(),
				}),
				response: {
					201: z.object({
						attendeeId: z.number(),
					}),
				},
			},
		},
		async (request, reply) => {
			const { eventId } = request.params;
			const { email, name } = request.body;

			const attendeeFromEmail = await prisma.attendee.findUnique({
				where: {
					eventId_email: {
						email,
						eventId,
					},
				},
			});

			if (attendeeFromEmail != null)
				throw new BadRequest("Email already registred in this event");

			// const event = await prisma.event.findUnique({
			//     where: {id: eventId}
			// })
			// const amountAttendeesForEvent = await prisma.attendee.count({
			//     where: {eventId}
			// })
            // OR

			const [event, amountAttendeesForEvent] = await Promise.all([
				prisma.event.findUnique({
					where: { id: eventId },
				}),
				prisma.attendee.count({
					where: { eventId },
				}),
			]);

			if (
				event &&
				event.maximumAttendees &&
				amountAttendeesForEvent >= event.maximumAttendees
			)
				throw new BadRequest("Event is full");

			const attendee = await prisma.attendee.create({
				data: {
					name,
					email,
					eventId,
				},
			});

			return reply.status(201).send({ attendeeId: attendee.id });
		}
	);
}
