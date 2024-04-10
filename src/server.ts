import fastifySwagger from "@fastify/swagger"
import fastifySwaggerUI from "@fastify/swagger-ui"
import fastifyCors from "@fastify/cors"
import fastify from "fastify";
import {
	serializerCompiler,
	validatorCompiler,
	jsonSchemaTransform
} from "fastify-type-provider-zod";
import { createEvent } from "./routes/create-event";
import { registerForEvent } from "./routes/register-for-event";
import { getEvent } from "./routes/get-event";
import { getAttendeeBadge } from "./routes/get-attendee-badge";
import { checkIn } from "./routes/check-in";
import { getEventAttendees } from "./routes/get-event-attendees";
import { errorHandler } from "./error-handler";

const app = fastify();

app.register(fastifySwagger, {
	swagger:{
		consumes: ["application/json"],
		produces: ["application/json"],
		info: {
			title: "pass.in",
			description: "Especificações da API para o back end da aplicação pass.in construida durante o NLW Unite da Rocketseat",
			version: '1'
		},
	},
	transform: jsonSchemaTransform,
})

app.register(fastifySwaggerUI, {
	routePrefix: "/docs"
})

app.register(fastifyCors, {
	origin: '*'
})

app.setValidatorCompiler(validatorCompiler)
app.setSerializerCompiler(serializerCompiler)

app.register(createEvent)
app.register(registerForEvent)
app.register(getEvent)
app.register(getAttendeeBadge)
app.register(checkIn)
app.register(getEventAttendees)

app.setErrorHandler(errorHandler)

app.listen({ port: 3333, host: '0.0.0.0' }).then(() => {
	// console.log("🌐 HTTP Server running")
	console.log("\x1b[32m🌐 HTTP Server running \x1b[0m");
});
