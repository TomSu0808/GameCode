using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class MouseLook : MonoBehaviour
{
    public bool usingMouse = true;

    public Transform playerBody;
    
    public float sensitivity = 1000f;

    float xRotation = 0f;
    float yRotation = 180f;

    // touch control
    Vector3 firstPoint, secondPoint;
    float tempXrotation, tempYrotation;

    // Start is called before the first frame update
    void Start()
    {
        Cursor.lockState = CursorLockMode.Locked;
    }

    // Update is called once per frame
    void Update()
    {
        if (usingMouse)
        {
            float mouseX = Input.GetAxis("Mouse X") * sensitivity * Time.deltaTime;
            float mouseY = Input.GetAxis("Mouse Y") * sensitivity * Time.deltaTime;

            xRotation -= mouseY;
            xRotation = Mathf.Clamp(xRotation, -90f, 90f);

            transform.localRotation = Quaternion.Euler(xRotation, 0f, 0f);
            playerBody.Rotate(Vector3.up * mouseX);
        }
        else
        {
            TouchControll();
            Rotation();
        }
    }

    public void TouchControll()
    {
        if (Input.touchCount > 0)
        {
            if (Input.GetTouch(0).phase == TouchPhase.Began)
            {
                firstPoint = Input.GetTouch(0).position;
                tempYrotation = yRotation;
                tempXrotation = xRotation;
            }
            if (Input.GetTouch(0).phase == TouchPhase.Moved)
            {
                secondPoint = Input.GetTouch(0).position;
                yRotation = (tempYrotation + (secondPoint.x - firstPoint.x) * sensitivity / Screen.width);
                xRotation = (tempXrotation + (secondPoint.y - firstPoint.y) * sensitivity / Screen.width);
            }
            if (Input.GetTouch(0).phase == TouchPhase.Ended)
            {
                tempYrotation = yRotation;
                tempXrotation = xRotation;
            }
        }
    }
    public void Rotation()
    {
        //xAngle = Mathf.Clamp(xAngle, -90f, 90f);
        xRotation = Mathf.Clamp(xRotation, -90f, 90f);
        playerBody.transform.rotation = Quaternion.Euler(Vector3.up * yRotation);
        transform.localRotation = Quaternion.Euler(-xRotation, 0f, 0f);
    }
}
