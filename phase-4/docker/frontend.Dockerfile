# Multi-stage build for the todo frontend
FROM node:18-alpine AS builder

WORKDIR /app

# Copy package files
COPY ../../phase-2/frontend/package*.json ./

# Install dependencies
RUN npm ci --only=production

# Copy application source code
COPY ../../phase-2/frontend .

# Build the Next.js application
RUN npm run build

# Production stage
FROM node:18-alpine

WORKDIR /app

# Create non-root user
RUN addgroup -g 1001 -S nodejs && \
    adduser -S nextjs -u 1001

# Copy built application from builder stage
COPY --from=builder --chown=nextjs:nodejs /app/public ./public
COPY --from=builder --chown=nextjs:nodejs /app/.next/standalone ./
COPY --from=builder --chown=nextjs:nodejs /app/.next/static ./.next/static

# Switch to non-root user
USER nextjs

EXPOSE 3000

ENV NODE_ENV=production

CMD ["node", "server.js"]