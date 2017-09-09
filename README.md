# PENNAPPS2017
request from client and corresponding replies:


    <1> student login request:
            <1><username><password>
        reply:
            on success: 200 <hash_id>
            on failure: 400 <No>

    <2> security login request:
            <2><username><password>
        reply:
            on success: 200 <hash_id>
            on failure: 400 <No>

    <3> student escort request:
            <3><student hash id><pickup location>
        reply:
            200 <Yes>

    <5> security confirm escort request:
            <5><student hash id><security hash id><estimated time>
        reply:
            on success: 200 <student info><security location>
            on failure: 400 <No>

    <6> security confirm pickup:
            <6><student hash id>
        reply:
            200 <Yes>

    <7> heart beat:
            <7><student/security hash id><location>
        reply:
            for student:
                if request is already confirmed:
                    200 <security info><estimated time>
                else:
                    400 <Yes>
            for security:
                if request is already confirmed:
                    200 <Yes>
                else:
                    <student hash id><pickup location>
                    <student hash id><pickup location>
                    ...
    <8> security refresh:
            <8>
        reply:
            <student hash id><pickup location>
            <student hash id><pickup location>
            ...

