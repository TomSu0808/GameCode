using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class PlatformMove : MonoBehaviour
{
    public List<Transform> points;
    public Transform platform;
    int goalPoint = 0;
    public float moveSpeed = 2;
 
    void Update()
    {
        MoveToNextPoint();
    }

    void MoveToNextPoint()
    {
        platform.position = Vector2.MoveTowards(platform.position, points[goalPoint].position, Time.deltaTime * moveSpeed);

        if (Vector2.Distance(platform.position, points[goalPoint].position) < 0.1f)
        {
            if (goalPoint == points.Count - 1)
                goalPoint = 0;
            else
                goalPoint++;
        }
    }
}
