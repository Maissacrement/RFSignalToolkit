# Android toolkit audit and prevent attack

## INTRODUCTION

First, I will introduce the working environment by talking about hardware constraints.
The recordings were made with a Samsung Galaxy S9+ using a magnetometer model "Magnetic Sensor, 1209-002401". The sensor expresses a magnetic field vector of format B(x,y,z) expressed in uT. For the moment I have no more information to bring you.
The objective from an application point of view is to get the most information from this signal. For that a file describing the signal is provided whose dataset can be improved if needed.

## Release

<table>
    <tbody>
        <tr>
        <th>ID</th>
        <th>Description</th>
        <th>Difficulté</th>
        <th>Priorité</th>
        </tr>
        <tr>
          <td>1</td>
          <td> 
            US1: As a User,<br>
            I want to be able to do a signal analysis.
            to do this, I go to the home page, I can choose to enter by hand or import a csv.
            I submit a set of data to the application, with the following parameters.
            <ul>
              <li> Magnet: Array ( < 50 integer, < 50 integer ) </li>
              <li> CreatedAtNs: Text ( < 50 char ) </li>
              <li> initialTime: Text ( < 50 char ) </li>
              <li> Time: Text ( < 50 char ) </li>
            </ul>
            Each set tagged by their axis in 3 rows x,y,z
            In order to retrieve the expression of the analyzed signal in graph form. 
          </td>
          <td>1</td>
          <td>HIGH</td>
        </tr>
        <tr>
          <td>2</td>
          <td> 
            US2: As a User,<br>
            I want to be able to select a specied range of frequency.
            to do this, i select with an input a data range. 
            In order to update data in analyzed signal. 
          </td>
          <td>1</td>
          <td>HIGH</td>
        </tr>
        <tr>
          <td>3</td>
          <td> 
            US3: As a User,<br>
            I want to be able to change format of data viz.
            to do this, i select in the input sinusoidal mode or numerical output.
            In order to, visualize in real time analyzed signal. 
          </td>
          <td>1</td>
          <td>LOW</td>
        </tr>
        <tr>
          <td>4</td>
          <td> 
            US4: As a User,<br>
            I want to be able to exploit signal datagrame header.
            to do this, A menu on the right with the data of the header,
            the datagram will allow to visualize the data in hexadecimal format
            In order to exploit the datagram provided.
          </td>
          <td>1</td>
          <td>LOW</td>
        </tr>
    </tbody>
</table>


