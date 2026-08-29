\# System Architecture



\*\*Project:\*\* Flagship UAV System

\*\*Document Version:\*\* 0.1

\*\*Date:\*\* 29 August 2026



\---



\## 1. Purpose



This document defines the initial high level system architecture for the Flagship UAV System.



The architecture describes the major subsystems, their responsibilities and the primary information flows between them.



The architecture is intended to provide a foundation for incremental development, testing and eventual transition from a virtual system to selected physical hardware.



The architecture will evolve as the system requirements become more detailed and individual subsystems are designed and tested.



\---



\## 2. Architectural Approach



The system will be developed using a virtual first approach.



Individual subsystems will initially be developed and tested using software simulations, mathematical models, synthetic data and authorised/public datasets where appropriate.



Once the virtual system has reached a suitable level of maturity, selected components will progressively be transitioned to physical hardware.



The system is divided into separate functional subsystems so that components can be developed, tested and modified independently where practical.



\---



\## 3. High-Level System Architecture



The system is based on multiple information sources that provide observations to the ground system and detection pipeline.



```text

&#x20;                        FLAGSHIP UAV SYSTEM





&#x20;    ┌──────────────────┐

&#x20;    │   UAV SUBSYSTEM  │

&#x20;    │                  │

&#x20;    │ Flight           │

&#x20;    │ Sensors          │

&#x20;    │ Navigation       │

&#x20;    │ Telemetry        │

&#x20;    └────────┬─────────┘

&#x20;             │

&#x20;             │ Telemetry

&#x20;             ▼

&#x20;    ┌──────────────────┐

&#x20;    │ COMMUNICATIONS   │

&#x20;    │                  │

&#x20;    │ Protocol         │

&#x20;    │ Integrity        │

&#x20;    │ Authentication   │

&#x20;    │ Encryption       │

&#x20;    └────────┬─────────┘

&#x20;             │

&#x20;             │

&#x20;             ▼

&#x20;    ┌──────────────────────────────────────┐

&#x20;    │           GROUND STATION             │

&#x20;    │                                      │

&#x20;    │  Telemetry     Database      GUI     │

&#x20;    │                                      │

&#x20;    └──────────────┬───────────────────────┘

&#x20;                   │

&#x20;                   │

&#x20;                   │

&#x20;    ┌──────────────┴───────────────────────┐

&#x20;    │                                      │

&#x20;    ▼                                      ▼

┌───────────────┐                    ┌────────────────┐

│ RF ANALYSIS   │                    │ OTHER SENSOR   │

│               │                    │ SOURCES        │

│ Signal        │                    │                │

│ Processing    │                    │ Future         │

│ Detection     │                    │ sensors        │

│ Features      │                    │                │

└───────┬───────┘                    └───────┬────────┘

&#x20;       │                                    │

&#x20;       │ RF observations                    │

&#x20;       └────────────────┬───────────────────┘

&#x20;                        ▼

&#x20;                 ┌───────────────┐

&#x20;                 │   TRACKING    │

&#x20;                 └───────┬───────┘

&#x20;                         ▼

&#x20;                 ┌───────────────┐

&#x20;                 │ CLASSIFICATION│

&#x20;                 └───────┬───────┘

&#x20;                         ▼

&#x20;                 ┌───────────────┐

&#x20;                 │ THREAT        │

&#x20;                 │ ASSESSMENT    │

&#x20;                 └───────┬───────┘

&#x20;                         ▼

&#x20;                 ┌───────────────┐

&#x20;                 │    ALERT      │

&#x20;                 └───────────────┘

```



The architecture separates information sources, communications, processing and operator-facing functions into distinct subsystems.



This allows individual components to be developed and tested independently while providing a path toward future sensor fusion and physical hardware integration.



\---



\## 4. Major Subsystems



\### 4.1 UAV Subsystem



The UAV subsystem represents the aircraft and its associated flight and sensing functions.



\#### Responsibilities



\* UAV flight simulation

\* Physical UAV integration

\* Flight state generation

\* Navigation

\* Sensor data

\* Position and movement information

\* Telemetry generation



\#### Primary outputs



The UAV subsystem will produce telemetry and other observations that can be consumed by the communications and analysis systems.



\---



\### 4.2 Communications Subsystem



The communications subsystem provides the communication path between the UAV and the ground station.



\#### Responsibilities



\* Telemetry transmission

\* Telemetry reception

\* Communication protocol

\* Packet handling

\* Data integrity

\* Authentication

\* Encryption

\* Communication fault detection

\* Communication performance monitoring



\#### Primary outputs



The communications subsystem provides validated telemetry to the ground station.



Communication conditions such as packet loss, latency and outages will also eventually be available to the monitoring and data systems.



\---



\### 4.3 Ground Station Subsystem



The ground station provides the central operator-facing environment for monitoring the system.



\#### Responsibilities



\* Telemetry reception

\* Telemetry processing

\* System monitoring

\* Data analysis

\* Event handling

\* Interaction with the database

\* Presentation of information to the operator

\* Display of alerts



The ground station should provide a common environment through which information from different subsystems can eventually be presented and correlated.



\---



\### 4.4 Database Subsystem



The database provides persistent storage for information generated by the system.



\#### Potential stored information



\* UAV telemetry

\* RF observations

\* Detection events

\* Tracks

\* Classification results

\* Anomalies

\* Threat assessments

\* Alerts

\* Communication events

\* System events



The specific database technology and schema will be selected during later design stages.



\---



\### 4.5 RF Analysis Subsystem



The RF analysis subsystem processes RF information within the virtual RF environment and, where appropriate, authorised physical RF sources.



\#### Responsibilities



\* Signal representation

\* Signal processing

\* Frequency-domain analysis

\* Signal characterisation

\* Feature extraction

\* Signal detection

\* RF observation generation



The initial RF environment will primarily use simulated signals and synthetic data.



The subsystem will eventually support analysis concepts including IQ data, FFTs and spectrograms.



\---



\### 4.6 Detection and Tracking Subsystem



The detection and tracking subsystem converts observations into detected objects and tracks.



\#### Responsibilities



\* Detection management

\* Object association

\* Track creation

\* Track updating

\* Track history

\* Correlation of observations



The subsystem should be capable of maintaining information about detected objects over time rather than treating every observation as an independent event.



\---



\### 4.7 Classification Subsystem



The classification subsystem evaluates detected objects using available characteristics and reference information.



\#### Responsibilities



\* Signal classification

\* Known/unknown determination

\* Identification of anomalous characteristics

\* Comparison against known expected characteristics

\* Classification confidence



The system should not automatically treat an unknown signal as hostile.



Unknown or anomalous observations will instead contribute to the later threat-assessment process.



\---



\### 4.8 Threat Assessment Subsystem



The threat assessment subsystem combines available evidence to produce an assessment of the detected object or situation.



Potential information sources include:



\* UAV telemetry

\* RF observations

\* Detection and tracking information

\* Classification results

\* Historical data

\* Other sensor observations



The assessment should provide a defined classification or threat status together with an appropriate confidence measure.



The exact assessment methodology will be developed later as the detection and sensor-fusion systems mature.



\---



\### 4.9 Graphical User Interface



The GUI provides the primary interface between the system and the operator.



\#### Responsibilities



\* UAV status display

\* Operational map

\* Detected object display

\* Track display

\* RF information

\* System status

\* Alerts

\* Historical information

\* Relevant threat-assessment information



The GUI should prioritise clear presentation of information rather than exposing unnecessary internal system complexity.



\---



\## 5. Primary Information Flows



\### 5.1 UAV Telemetry



```text

UAV

&#x20;↓

Telemetry Generation

&#x20;↓

Communications

&#x20;↓

Ground Station

&#x20;↓

Database / Analysis / GUI

```



Telemetry will provide information about the UAV's current state and historical behaviour.



\---



\### 5.2 RF Analysis



```text

Simulated RF Environment

&#x20;↓

RF Analysis

&#x20;↓

Signal Characterisation

&#x20;↓

Signal Detection

&#x20;↓

RF Observations

```



The RF analysis subsystem will convert simulated RF information into structured observations that can be used by downstream detection and assessment systems.



\---



\### 5.3 Detection and Tracking



```text

RF Observations

&#x20;      +

Other Sensor Observations

&#x20;      ↓

Detection

&#x20;      ↓

Object Association

&#x20;      ↓

Tracking

&#x20;      ↓

Track History

```



The system will eventually support multiple observations contributing to the same detected object or track.



\---



\### 5.4 Classification



```text

Track

&#x20; +

RF Characteristics

&#x20; +

Reference Information

&#x20;      ↓

Classification

&#x20;      ↓

Known / Unknown / Anomalous

&#x20;      ↓

Classification Confidence

```



Classification results will contribute to threat assessment rather than being treated as an absolute determination of intent.



\---



\### 5.5 Threat Assessment



```text

Telemetry

&#x20;   +

RF Observations

&#x20;   +

Tracks

&#x20;   +

Classification

&#x20;   +

Historical Data

&#x20;   +

Other Sensor Data

&#x20;         ↓

&#x20;    Threat Assessment

&#x20;         ↓

&#x20;   Threat Status

&#x20;         +

&#x20;      Confidence

&#x20;         ↓

&#x20;       Alert

```



This represents the eventual sensor-fusion concept of the system.



The exact algorithms and weighting of information sources will be developed and tested later.



\---



\### 5.6 Operator Situational Awareness



```text

Telemetry

&#x20;    +

RF Observations

&#x20;    +

Tracks

&#x20;    +

Classification

&#x20;    +

Threat Assessments

&#x20;    +

Historical Data

&#x20;         ↓

&#x20;     Ground Station

&#x20;         ↓

&#x20;         GUI

&#x20;         ↓

&#x20;      Operator

```



The purpose of this flow is to provide the operator with a consolidated representation of the system state and detected activity.



\---



\## 6. Subsystem Interfaces



Subsystem interfaces define how information moves between components.



Initial interfaces include:



| Interface  | Source            | Destination       | Information              |

| ---------- | ----------------- | ----------------- | ------------------------ |

| IF-UAV-COM | UAV               | Communications    | Telemetry                |

| IF-COM-GS  | Communications    | Ground Station    | Validated telemetry      |

| IF-RF-DET  | RF Analysis       | Detection         | RF observations          |

| IF-DET-TRK | Detection         | Tracking          | Detection observations   |

| IF-TRK-CLS | Tracking          | Classification    | Track information        |

| IF-CLS-TA  | Classification    | Threat Assessment | Classification results   |

| IF-TA-GUI  | Threat Assessment | GUI               | Threat status and alerts |

| IF-GS-DB   | Ground Station    | Database          | Telemetry/events         |

| IF-DB-GS   | Database          | Ground Station    | Historical information   |



These interfaces are currently conceptual.



The exact protocols, data formats and implementation mechanisms will be defined during later subsystem design.



\---



\## 7. Architectural Principles



The architecture follows the following principles:



\### 7.1 Separation of Responsibilities



Each subsystem should have a clearly defined purpose.



\### 7.2 Modularity



Subsystems should be independently developable and testable wherever practical.



\### 7.3 Defined Interfaces



Subsystems should communicate through defined interfaces rather than relying on undocumented internal behaviour.



\### 7.4 Virtual-First Development



Software simulations should be used to develop and validate system behaviour before physical implementation wherever practical.



\### 7.5 Testability



Subsystems and interfaces should be designed so that their behaviour can be independently tested.



\### 7.6 Traceability



Implementation and testing should eventually be traceable back to defined system requirements.



\### 7.7 Expandability



The architecture should allow additional sensor sources and processing capabilities to be introduced without requiring a complete redesign.



\---



\## 8. Initial Architectural Constraints



The architecture is subject to the following constraints:



\* Physical implementation should make maximum practical use of existing hardware.

\* Additional hardware should only be introduced where genuinely necessary.

\* Initial RF development should primarily use simulated and synthetic signals.

\* Physical RF work must remain within appropriate legal and regulatory boundaries.

\* The system should be capable of operating as a complete virtual system before physical integration.

\* The architecture must remain practical for development on available computing resources.



\---



\## 9. Architectural Assumptions



The current architecture assumes that:



\* UAV telemetry can initially be generated entirely in software.

\* RF signals can initially be generated and analysed virtually.

\* Multiple subsystems can be implemented and tested independently.

\* Physical hardware can eventually replace selected simulated components.

\* Requirements and subsystem interfaces may change as development progresses.



\---



\## 10. Future Architecture Development



The architecture will be expanded progressively as the project develops.



Future design work will include:



\* Detailed UAV architecture

\* Telemetry data structures

\* Communications protocol

\* Network architecture

\* Ground-station architecture

\* Database schema

\* RF processing pipeline

\* Detection algorithms

\* Tracking methodology

\* Classification methodology

\* Sensor-fusion architecture

\* Security architecture

\* Testing architecture

\* Physical hardware architecture



Detailed design decisions will be documented separately from this high-level architecture.



\---



\## 11. Current Architectural Status



\*\*Version 0.1 — Initial Architecture Baseline\*\*



The current document defines the initial high-level system architecture and conceptual subsystem interfaces.



The architecture is not considered final.



Future revisions will be made when detailed subsystem design, implementation and testing provide evidence that architectural changes are required.



