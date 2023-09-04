# AIRCRAFT WEIGHT AND BALANCE CALCULATOR
  
#### Video Demo:  [Introduction Video](blahvid.youtube)

### Description:

#### Introduction:

This program was created by **William Shearer**, from Quito, Ecuador, for the final project of the **2022 HarvardX CS50X** online course.
The program is the **Aircraft Weight and Balance Calculator**. It is a simplified, console program that allows the user determine the center of gravity (CG), and other weight related limitations, of an aircraft.
The program is written exclusively in **Python 3**. External libraries used are; pandas 1.5.1.

#### Project Contents:

The project directory includes the following files necessary to run the program:
- acwbclass.py
    - A Python file that contains a custom class, AircraftWB.
- test_acwbclass.py
    - A Python unittest class for functionality control of the class methods.
- cs50xproject.py
    - The main program that utilizes the acwbclass to implement a weight and balance computer.
- README.md
    - This file. A description of the project.
- requirements.txt
    - A file that was generated automatically to point the user to any imported externals (in this case, only pandas).
- reference.txt
    - A file that contains the data needed to create two aircraft, to start the user off.

#### Aircraft Weight and Balance Overview:

The user can create custom aircraft configurations for weight and balance calculations. It is recommended that the user refer to an official OEM aircraft document, like the POH or FCOM, to obtain real data. Once an aircraft configuration has been created, the user may **save** the aircraft as an afc file in the cwd for future use, or proceed immediately to perform **W&B calculations**. Saved files may be **loaded** in the future for convenience, avoiding having to create the aircraft configuration from scratch again.

The configuration of an aircraft for W&B calculations contains several parts, as follows:

- **Calculation Standard Units**
    - These are the baseline standards that should be applied to the aircraft. They include the units required to input data in capacities of **U.S. gallons** or **litres**, weights in **pounds** or **kilograms**, and measure distances in **inches**, **feet**, **centimeters**, or **meters**. The user is responsible for ensuring that the data is entered in the corresponding units.

- **Basic Aircraft Weights**

    - Aircraft have certain critical weights that the OEM establishes during the design and testing processes of the type. These are documented, and provided to the users of the product. They are to be considered **limitations**, and are documented as such. The program permits the user to enter this data during the configuration (creation) phase. Important weights are:

        - **Basic Empty Weight**: This is the empty weight of a particular aircraft. Included in it is the weight aircraft itself, minus fuel in the tanks, passengers, and cargo. Residual fluids and non-consumable fluids (for example, hydraulic fluid) are included. It may also be known as the **Manufacturer's Empty Weight**.

        - **Maximum Zero Fuel Weight**: Fuel on board an aircraft is a consumable weight. This means that the aircraft will change weight (reduction) as it flies. Its landing weight, as a result, may be considerably different to its take off weight. The OEM established a maximum structural weight for the aircraft that is equal to a fully loaded aircraft, minus all the fuel. The value of this weight may be different from the maximum structural weight considering fuel on board. **MZFW**, where established, will always be less than the maximum structural weight of the aircraft considering fuel on board. Not all aircraft have a MZFW. Where an aircraft does not have a MZFW, this value can be considered to be equal to the maximum structural gross weight, with fuel, but never more.

        - **Maximum Take Off Weight**: The maximum structural weight permitted for the aircraft to initiate a take off. If the wieght exceeds the value of MTOW, the user must reduce weight either by subtracting fuel, pasengers (Pax), or cargo, until the weight is at or below **MTOW**. A word of caution. Complying with MTOW does not automatically mean that the take off will be safe, as other environmental factors may impose a necessity to further reduce weight. However, under no circumstance may an aircraft attempt a take off if its weight is over MTOW, or a hazardous flight condition will, very definately, be the result.

        - **Empty Moment**: To calculate a center of gravity along an aircraft's longitudinal axis, just knowing the weight of the aircraft is not sufficient. Each weight added, be it fuel, passengers, or cargo, at different points along the longitudinal axis will cause the aircraft to become heavier towards the nose or tail. Where the weight is added will influence this tendency. It is therefore necessary for the OEM to establish a reference point, known as the **datum**, from which the distance, known as an **Arm**, will determine what effect adding a weight will have on the center of gravity. Moment will be calculated by multiplying the arm by the weight added at that position. An empty aircraft will have a specific balance point where the weight on one side of it will be equal to the weight on the other. Effectively, this is the center of gravity (CG). It will be at a specific distance from the datum. That distance multiplied by the empty weight of the aircraft will provide an Empty Moment. The user may then use this data to calculate the shift of the CG, forward or aftwards, as new weights are added to the aircraft at determined arms.

- **Fuel Tanks**

    - Quantity of fuel is usually expressed in volumetric measurements, such as gallons or litres. In aircraft, however, that measurement must be converted to a weight for the purposes of effectively calculating W&B. To accurately obtain a weight equivalent to a given measurement of volume, the fuel's density must be known. Here, we encounter another requirement. Aircraft, depending on their propulsion systems (gas turbine or reciprocating engines), use fuels of different densities: **Jet Fuel** or **AvGas**, respectively. Once the correct weight has been derived from a given quantity, the W&B procedure may continue as normal.

- **Pax/Crew Sections**

    - The weight of the persons who make up the crew and passengers of an aircraft may vary widely. It is impractical, however, to individually weigh each person on a scale before a flight. To this end, there is a standard weight considered for each person on board an aircraft, this being 170 lb. It is also considered that the person has a baggage or equipment allowance of 20 additional pounds. Therefore, the weight of crew/passengers on an aircraft is the result of the number of persons multiplied by 190 lb. It is important to note, however, that the aircraft's limitation remains in weight. Therefore, passenger section limits of an aircraft are determined in a load (weight), and the sum of the weight of the number of passengers must not exceed that load. The maximum number of seats in a section would, therefore, be determined by the weight of that many persons, at a standard weight, not exceeding the load limit.

- **Cargo Sections**

    - Cargo is declared and loaded on an aircraft as a weight. There are no conversions necessary. The only precaution is to ensure that the weight that is declared is in equivalent units to the system that will be used to determine the aircraft's W&B.

- **CG Limits**

    - The entire purpose of determining a true CG position, for each and every flight, is based on the fact that the CG has limits. These limits are **forward** and **aft**, at a given and determined distance from the datum. The aircraft *must not* be operated with the true CG outside of these limits, or a dangerous flight condition will result.

#### Program Usage:

The program is run by moving to the working directory that contains the Python script *cs50xproject.py*, and entering *python cs50xproject.py* on the command line. The options presented will be:

1. Create New Aircraft
2. Load Aircraft
3. Save Aircraft
4. Set and Calculate W&B
5. Exit

The user may execute any of the options by entering the corresponding number on the prompt and hitting ENTER. A detailed description of each option follows:

#### MAIN MENU

##### Create new Aircraft:

An example for creating a **Pilatus PC-12** in **passenger configuration** will be used during this description of program usage.

**Aircraft Type**

The user will be prompted to enter the aircraft **Type**. This is important because it will be the name of the file, if the user elects to save the configuration after the aircraft is created. Where different configurations of the same aircraft will be created, it will be important to differentiate the versions. For example, a PC-12 may have cargo and passenger configurations. It would be suggested to create each as PC-12_pax and PC-12_cargo. As these will be filenames, some discipline in entering them should also be effected. Avoid extra long names, and use underscores instead of spaces. Avoid special characters, such as parenthesis, ampersands, etcetera.

*Type **PC-12_pax**, and hit ENTER.*

**Unit Options**

The user will be prompted to select the **measurements standard** to be used for this aircraft. Select as appropriate, entering the corresponding number on the prompt and hitting ENTER. All future entries of data for this aircraft *must* conform to this standard. Selecing an invalid option will cause a reprompt.

*Select **4**, and hit ENTER.*

**Fuel Option**

The user will be prompted to select the appropriate **Fuel** for the aircraft. Enter the number for the correct fuel type on the prompt, and hit ENTER. Selecing an invalid option will cause a reprompt.

*Select **1**, and hit ENTER.*

**Basic Weight Data**

The user will be prompted to enter, in order, **Empty Weight**, **Empty Moment**, **MZFW**, and **MTOW**. This is basic aircraft data available in the official aircraft documentation. The entries should be integers or floating point numbers. No characters are allowed. Attempting to enter an alpha or special character will result in a reprompt.

*For Basic Empty Weight, type **2545**, and hit Enter.*

*For Basic Empty Moment, type **14557.4**, and hit ENTER.*

*For Maximum Zero Fuel Weight, type **3700**, and hit ENTER.*

*For Maximum Take Off Weight, type **4100**, and hit ENTER.*

The user will be asked if the data is correct. This is a chance to review the entered data. If any of it is incorrect, enter **N** (or any other character except Y). The user may start again at the beginning of the basic weight data entry procedure. Otherwise, commit the data by entering **Y**.

**Set Number of Sections for Fuel, Crew/Pax, and Cargo**

The user will be prompeted to enter the actual number of each type of section. Zero is an acceptable answer in any of the categories. Negative numbers or characters other than integers will be rejected, and the user reprompted.

*For Number of Fuel Tanks, enter **2**, and hit ENTER.*

*For Number of Crew/Pax sections, enter **6**, and hit ENTER.*

*For Number of Cargo Sections, enter **1**, and hit Enter.*

The user will be asked if the data is correct. Enter **Y**, if so, to continue.

**Create Fuel Tanks**

The user will be asked to determine the characteristics of each fuel tank. Note, there are two *alternate* ways to enter this data. In this example, both ways will be demonstrated, as follows:

The user may directly enter the **maximum capacity**, in the corresponding unit of volume, and the **maximum moment**.

- For Tank 1:

    - *Enter **611.1 3599.4**, exactly as shown, on the same line, separated by a space, and hit ENTER.* The first figure is the maximum capacity of the tank, in litres, and the second is the maximum moment, in kg/m.

The user may enter the maximum capacity and the arm to the tank, separated by an **" x "**.

- For Tank 2:

    - *Enter **611.1 x 5.89**, exactly as shown, on the same line, separated by a space, an **x** and another space. Hit ENTER.* The first figure is the maximum capacity of the tank, in litres, and the second means that the values must be multiplied, and the third figure is the **arm**, in meters.

The reason there are alternate methods is because aircraft documentation differs, from type to type. Some provide the maximum moment, others provide the arm. Some provide both, but in any case, one or the other is provided. This feature gives the user the flexibility to enter the data in accordance with the documentation provided information.

Between the creation of each tank, the user will be prompted to confirm that the data is correct. Type **Y** and hit ENTER, if so. If the data is incorrect, there is a chance to correct it by entering **N**.

**Create Crew/Pax Sections**

The user will be prompted to configure each of the crew/passenger sections. The user must enter the maximum weight (permissible load), in the selected unit of weight, for the section, and the maximum moment. Conversely, the user may enter the maximum weight multiplied by the arm, similar to the alternate procedure with the fuel tanks. In the example, both methods will be demonstrated.

- *For C/P section 1, enter **240 x 4.07**, and hit ENTER.*

- *For C/P section 2, enter **240 1300.8**, and hit ENTER.*

- *For C/P section 3, enter **240 x 6.26**, and hit ENTER.*

- *For C/P section 4, enter **240 1706.4**, and hit ENTER.*

- *For C/P section 5, enter **240 1905.6**, and hit ENTER.*

- *For C/P section 6, enter **120 x 8.74**, and hit ENTER.*

Between each entry, the user will be asked to confirm that the data is correct, as before.

**Create Cargo Sections**

The user will be prompted to creste the cargo sections. The procedure is the same as the crew/pax data entry. Enter maxmum weight, in the corresponding unit, and the moment, or enter the weight and the arm, separated by an " x '.

- *For Cargo Section 1, enter **180 1695.6**, and hit ENTER.*

The user will be prompted if the data is correct. Enter **Y** to confirm.

**Set CG Limits**

The user will be prompted to enter the CG limits, in the distance unit. Use negative numbers for forward of datum, and positive number for aft of datum. Hint: most aircraft have the limits established aft of datum (AoD).

- *For Forward CG Limit, enter **5.69**, and hit ENTER.*

- *For Aft CG Limit, enter **6.17**, and hit ENTER.*

Again, the user will have the opprotunity to review and correct any mistakes. After confirming with **Y**, the user will be presented with a table of all the entered data. The aircraft will be configured, and the user may save it if the data is correct (option 3 on the **Main Menu**).

##### Load Aircraft

From option 2 on the **Main Menu**, the user may load a previously saved aircraft. If an aircraft is saved, there is no need to create a new one. The aircraft will be loaded with all operational values zeroed, ready for setting up with option 4 on the **Main Menu**.

Select **2** on the prompt. A list of saved aircraft will be displayed. Select the number of the corresponding aircraft. It will be loaded, and a table showing the aircraft data will be displayed. Hit ENTER to continue.

If no aircraft were previously saved, the program will inform the user, and return to the Main Menu.

##### Save Aircraft

From option 3 on the **Main Menu**, the user may save the last aircraft that was created with option 1. If no aircraft has been created, the program will inform the user that there is no aircraft to save, and return to the Main Menu.

##### Set and Calculate W&B

From this option, the user may set the aircraft's operational weights for a flight. Bear in mind the following:

- Fuel must be entered in the corresponding capacity, up to or less than the maximum capacity that was configured when the aircraft was created.

- Crew and Passengers must be entered as a number of persons, up to or less than the maximum seating. Note that the maximum seating is a function of the maximum load configured for the section, divided by the standard weight for persons, rounded down to the nearest integer. So, for the PC-12, Pax section 2, the maximum weight is 240 kg. The standard weight of each person (including baggage) is 86 kg. 240 / 86 = 2.79. Therefore, 2 persons, maximum. In any event, the program does not allow the user to enter a number of passengers greater than the limit, which it has already calculated internally.

- Cargo must be entered as the actual weight of the cargo, in the correponding unit of weight.

An example with the previouslycreated PC-12. Form the **Main Menu**, select option **4**. The user will be prompted to enter the capacity of Jet Fuel to be loaded into each of the tanks, in turn. Remember, the units will be litres, and the maximum was 611.1.

- *For Tank 1, enter **357.5**, and hit Enter.*

- *For Tank 2, enter **342.3**, and hit ENTER.*

The user will be prompted to confirm the quantity is correct after each entry. Entering **Y** will confirm. Next, the program will ask for the number of crew/pax for each of the six sections.

- *For C/P section 1, enter **2** and hit ENTER.*

- *For C/P section 2, enter **0** and hit ENTER.*

- *For C/P section 3, enter **0** and hit ENTER.*

- *For C/P section 4, enter **1**, and hit ENTER.*

- *For C/P section 5, enter **2**, and hit ENTER.*

- *For c/P section 6, enter **1**, and hit ENTER.*

Again, after each entry, the user will be prompted to confirm the data is correct. Next, the program will ask the user to input the weight of the cargo on board, in the aft cargo section. In this example, we will place the maximum permissible load in the section, 180 kg.

- *For Cargo section 1, enter **180**, and hit ENTER.*

Confirm that this is the desired amount of cargo. Once the cargo has been confirmed, a table showing the aircraft's loading will be displayed. At the bottom, in NOTES, the position of the CG is displayed. If ever the aircraft is out of CG limits, is above MTOW with fuel, or above MZFW without fuel, corresponding WARNING messages will also be displayed under NOTES, to warn the crew that the aircraft is unsafe.

##### Exit

Terminates the program and returns to the command line.

#### Program Limitations

This program accurately calculates the aircraft CG, provided the user adheres to maintaing the correct units while entering data. If the user suddenly starts entering data in pounds for a kilogram standard aircraft, the data will not be reliable. Care must be taken, regarding this. The program maintains safeguards that prevent the user from entering fuel quantities, passengers, or cargo in excess of the maximum limits, per section, also provided that the user is entering data with reference to the correct units.

One of this program's limitations is the CG limit envelope. Some aircraft have CG limits that change as the weight is varied. In future versions of this program, this feature will be implemented. For the time being, the CG limits should be entered as the most likely, for normal operation, or the most critical.

Another limitation is shifting arms for fuel tanks. Because of the shape of some aircraft's fuel tanks (often placed in the wings, and conforming therefore to the shape of), filling of the tanks is not an even process. This means that the arm of the tank is variable, relative to how much fuel is in the tank. More often than not, the change is small, almost negligible. however, it is a factor, and will be implemented in future versions.

#### Further reading

For those interested, more information regarding Aircraft Weight and Balance can be obtained in the FAA document, No. FAA-H-8083-1B, available free to the public at this official link:

[Weight and Balance Handbook](https://www.faa.gov/regulations_policies/handbooks_manuals/aviation/media/faa-h-8083-1.pdf)

#### Programming Notes

This program was created exclusively for the **HarvardX CS50** course. The author was relatively familiar already with some programming languages, for example C, Lua, and HTML/CSS/JavaScript. However, Python 3 proved to be a very unpleasant surprise, and made very little sense on first contact, during the course. It bore absolutely no similarity to anything the author had ever seen before, and appeared to have a philosophy that was at odds with everything that had previously constituted good programming habits.

Therefore, the author decided to face his weakness, and create the final project as a command line Python 3 program. Some of the unusual features of Python the author concentrated on getting experience with were:

- Classes (especially, properties and decorators)
- Multiple argument return from functions (tuples)
- List comprehensions
- Lambda
- Exceptions (try: except:)
- Lists and dictionaries
- Assignement of functions to lists
- Pickle dump and load, and file access / creation
- Pandas
- Regex
- List duplication and copy (deepcopy)

The heart of the program is the **AircraftWB** class, created in the *acwbclass.py* file. The *cs50xproject.py* file simply pulls the class together in an interface, to create the final result that the user sees and interacts with. It was the author's desire to deepen the understanding of Python's implementation of OOP, hence the class creation. The program could, quite easily, have been made without the inclusion of this class. That said, creating the class was, indeed, a benefit, and did facilitate the creation of the program. Therefore, it was a positive experience. The author continues to learn the Python language, and his best guess is that in a short time into the future, he could code this program with even greater efficiency.

Due to the fact that the class is fairly critical, a *test_acwbclass.py* was implemented to control the changes that were necessarily made during development. This test file is made with a separate, unittest class, and tests each of the AircraftWB class member functions for correct functionality. It plays no part in the running of the program itself, but is included in the final upload, as it would help any users who may alter the class maintain its correct and expected function.

There is one external, pandas 1.5.1, which was imported to the project to create the visual data table of aircraft information. All other modules used are part and parcel of Python 3.

#### Bug Reports

[GitHub AircraftWB](https://github.com/William-Shearer/AircraftWB/tree/master)
