---

title: "SANS DFIR101: Digital Forensics Essentials"

description: "A write-up for SANS Digital Forensics webinar"

pubDate: "June 9, 2024"

heroImage: "/linux.png"

tags: ["courses", "cybersecurity"]

---

  

# SANS DFIR101: Digital Forensics Essentials

  

### What is Digital Evidence

  

- Digital evidence is simply the information that is stored or transmitted in a digital format that may be of value to an investigation

  

### Data vs Metadata

  

- **Data** is "information based in digital form that can be transmitted or processed"[1]

- **Metadata** is "information that provides information about other data"[2]

  - **Types of Metadata**

    - **Filesystem Metadata (Filesystem Dependent)**

      - Example: filename, file creation datetime, file content modification datetime

      - **File Data**

        - The actual contents of a particular file

      - **File Metadata (File Type Dependent)**

        - Example: last printed datetime, author, last saved, etc.

  

### Nature of Digital Evidence

  

- In order to understand digital evidence and correctly interpret its potential relevance to an investigation, it is vitally important to understand how this evidence is stored on a device.

- #### How Data is Stored

  #### **Applications --> Operating System --> Filesystem --> Sectors and Clusters --> Bits and Bytes**

  - Data is stored on a device in binary; that is, zeroes and ones

    - A single zero/one is called a "bit"

    - Bits are grouped into sets of eight, called "bytes"

  - Numbering Systems

    - In decimal, we have "base10"

    - In Hexidecimal (or hex), we have base16

  - **Sectors**

    - Data on a disk is stored in sectors and clusters

    - The number of bytes in a sector is defined in the filesystem header

      - Example: NTFS (512 byte sector), APFS (512 byte sector)

  - **Allocated and Unallocated Space**

    - Each cluster is labeled by the OS as either allocated or unallocated:

      - **Allocated:** cluster is currently allocated to a file

      - **Unallocated:** cluster is NOT currently allocated to a file

    - An unallocated cluster does NOT indicate it has never been previously allocated to any files

  - **Slack Space**

    - Since a cluster is the smallest addressable space, a new file is created in one or more clusters.

    - If the entirety of this space is not occupied by the file, remaining space cannot be used by another file.

    - The remaining space is called "**slack space**"

  - **Types of Slack Space**

    - **RAM Slack**: unused space between the end of the logical file and the end of that sector

    - **File Slack**: unused sectors within the last cluster the file occupies.

    - **Volume Slack**: unused space between the end of the filesystem and the end of the partition that it occupies.