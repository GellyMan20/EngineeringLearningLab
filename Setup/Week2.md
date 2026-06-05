```text
NOTE: crtl+shift+V to preview markdown file
NOTE: ctrl+K V to view and preview markdown
```

# Week 2 – Cloud & Telemetry Foundations for Aerospace Systems

## Theme

**Understanding Cloud, Telemetry, and Distributed Systems**

### Primary Goal

Develop a practical understanding of how modern aerospace, autonomy, and ground systems exchange data, process telemetry, monitor health, and leverage cloud infrastructure.

By the end of this week, you should understand how data moves from a vehicle through a network to operators and services, and be able to build a simple telemetry pipeline yourself.

---

# Learning Objectives

Understand:

- Cloud fundamentals
- Client-server architectures
- APIs
- Telemetry systems
- Distributed systems
- Observability
- Basic cloud services
- System architecture concepts

---

# Technical Accomplishments

## 1. Learn API Fundamentals

### Topics

- REST APIs
- HTTP
- Request/Response Model
- JSON Data Formats

### Key Concepts

```text
GET
POST
PUT
DELETE
Status Codes
Headers
Payloads
```

### Success Criteria

Able to explain:

- What an API is
- Why APIs exist
- How systems communicate through APIs
- Difference between GET and POST

---

## 2. Learn Client-Server Architecture

### Topics

- Clients
- Servers
- Services
- Endpoints

### Aerospace Examples

```text
Aircraft → Ground Station

Ground Station → Cloud Service

Cloud Service → Operator Dashboard
```

### Success Criteria

Able to draw:

```text
Client
   ↓
Server
   ↓
Database
```

and explain the role of each component.

---

## 3. Learn Telemetry Fundamentals

### Topics

- Telemetry generation
- Telemetry transmission
- Telemetry storage
- Telemetry visualization

### Example Telemetry Message

```json
{
  "timestamp": 123.4,
  "latitude": 38.90,
  "longitude": -77.04,
  "altitude": 5000,
  "airspeed": 120
}
```

### Success Criteria

Able to explain:

- What telemetry is
- Why telemetry is important
- Common telemetry fields
- How telemetry moves through a system

---

## 4. Learn Distributed Systems Concepts

### Topics

- Services
- Data Flow
- Availability
- Reliability

### Key Concepts

```text
Producer
Consumer
Message
Service
Network
```

### Success Criteria

Understand:

- Why distributed systems exist
- Benefits and drawbacks
- Common failure modes

---

## 5. Learn Observability

### Topics

- Logs
- Metrics
- Traces
- Alerts

### Examples

```text
CPU Usage

Memory Usage

Messages Received

Latency

Packet Loss
```

### Success Criteria

Able to explain:

- Difference between logs and metrics
- What monitoring accomplishes
- Why observability matters

---

# Engineering Projects

## Project 1 – Telemetry Generator

### Objective

Simulate a vehicle producing telemetry.

### Inputs

Generate:

- Position
- Velocity
- Altitude
- Heading

### Example Output

```json
{
  "time": 10,
  "lat": 38.90,
  "lon": -77.04,
  "altitude": 5000,
  "airspeed": 120
}
```

### Success Criteria

Generate telemetry once per second.

---

## Project 2 – Telemetry Receiver

### Objective

Receive telemetry messages through a REST API.

### Architecture

```text
Telemetry Generator
          ↓
        API
          ↓
Telemetry Receiver
```

### Success Criteria

Messages successfully received and displayed.

---

## Project 3 – Data Storage

### Objective

Store telemetry.

### Options

```text
CSV
```

or

```text
SQLite
```

### Success Criteria

Historical telemetry can be retrieved and viewed.

---

## Project 4 – Health Dashboard

### Objective

Create a simple monitoring display.

### Display

```text
Messages Received

Last Contact Time

Latency

Packet Count
```

### Success Criteria

Dashboard updates as telemetry arrives.

---

# Architecture Exercises

## Context Diagram

Create a high-level diagram showing:

```text
Vehicle

Ground Station

Cloud Services

Operator
```

### Success Criteria

Major interfaces identified.

---

## Telemetry Flow Diagram

Create:

```text
Vehicle
   ↓
Network
   ↓
API
   ↓
Storage
   ↓
Dashboard
```

### Success Criteria

End-to-end flow documented.

---

## Deployment Diagram

Identify:

```text
Client Device

Server

Database
```

### Success Criteria

Understand where software executes.

---

# Documentation Accomplishments

## Create Notes

### File

```text
notes/cloud-concepts.md
```

### Include

- APIs
- REST
- Telemetry
- Client-server architectures
- Distributed systems
- Observability

---

## Create Architecture Notes

### File

```text
notes/system-architecture.md
```

### Include

- Context diagrams
- Deployment diagrams
- Data flows
- Interface definitions

---

# Git Accomplishments

Continue:

```bash
git status
git add
git commit
git push
```

### Example Commits

```text
Created telemetry generator

Added REST API receiver

Implemented telemetry storage

Created architecture diagrams

Completed cloud notes
```

---

# Aerospace Relevance

This week directly supports:

- Ground systems engineering
- Telemetry architectures
- Health monitoring
- Fleet operations
- Distributed autonomy
- Cloud-enabled aviation systems
- AWS/Azure discussions
- Service-oriented architectures

---

# AI Integration Opportunities

Potential future integrations:

- Telemetry anomaly detection
- Health monitoring agents
- Failure prediction
- Fleet optimization
- Mission analytics

No AI implementation required this week.

Focus on understanding the infrastructure AI systems operate within.

---

# Monte Carlo / Operational Analysis Integration

Perform simple analyses such as:

### Message Latency

```text
Average Latency

Maximum Latency

Minimum Latency
```

### Message Loss

```text
Messages Sent

Messages Received

Loss Percentage
```

### Failure Modes

```text
Network Loss

Service Crash

Data Corruption
```

Document observations.

---

# Engineering Artifact

Produce:

## Diagrams

- Context Diagram
- Telemetry Flow Diagram
- Deployment Diagram

## Documentation

- Cloud Concepts Notes
- Architecture Notes

## Software

- Telemetry Generator
- Telemetry Receiver
- Data Storage
- Health Dashboard

---

# Week 2 Definition of Success

You can confidently explain:

- What a REST API is
- What telemetry is
- What observability means
- What a distributed system is
- How cloud services communicate
- How aerospace telemetry pipelines work

And demonstrate:

```text
Telemetry Generator
        ↓
REST API
        ↓
Receiver
        ↓
Storage
        ↓
Dashboard
```

running locally on your machine.

---

# Stretch Goals (Excellent Outcome)

## Explore AWS

Learn:

```text
EC2
S3
Lambda
CloudWatch
API Gateway
```

Understand what problem each service solves.

---

## Containerize the System

Install Docker and run:

```text
Telemetry Generator

Telemetry Receiver
```

inside containers.

---

## Create a Simple Cloud Deployment Diagram

Show how your system might scale to:

```text
Multiple Vehicles

Cloud Services

Operator Dashboards
```

---

# Why Week 2 Matters

Modern aerospace systems are increasingly software-defined and cloud-connected.

Whether working on:

- UAS
- Space Systems
- Ground Systems
- Autonomy Platforms
- Health Monitoring Systems

you will encounter:

- APIs
- Telemetry
- Distributed Architectures
- Cloud Infrastructure
- Observability

This week establishes the foundation for understanding how information moves through complex aerospace systems before diving into dynamics, simulation, controls, and autonomy.